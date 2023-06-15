import os
import subprocess
import glob
import tempfile

def running_proteins_structure (_dir, SCREEN, DATABASE, HEADN, ANNOT):
    print('*'*64, 'inside running proteins structure')
    os.chdir(_dir+'/content/input')
    if os.path.isfile(f'{_dir}/content/result/result.tab'):
        os.remove(f'{_dir}/content/result/result.tab')
    if os.path.isfile(f'{_dir}/content/result/tmalign_formatted.tab'):
        os.remove(f'{_dir}/content/result/tmalign_formatted.tab')
    if os.path.isfile(f'{_dir}/content/result/fatcat_formatted.tab'):
        os.remove(f'{_dir}/content/result/fatcat_formatted.tab')
    if os.path.isfile(f'{_dir}/content/result/lovoalign_formatted.tab'):
        os.remove(f'{_dir}/content/result/lovoalign_formatted.tab')

   
    if SCREEN == "foldseek":
        for f in os.listdir():
                os.system(f"{_dir}/content/programs/foldseek/bin/foldseek easy-search {f} {_dir}/content/foldseek_data/fs_{DATABASE} {_dir}/content/result/screening/tmp.tab.fmt {_dir}/content/tmpFolder --max-seqs {HEADN} -e inf")
                os.system((f"cut -f 1,2 {_dir}/content/result/screening/tmp.tab.fmt | sort | uniq | perl -ne '@a = split(/\\./, $_); print join(\".\", @a[0 .. $#a-1]).\"\\n\";' > {_dir}/content/result/screening/{f}.tab.fmt"))
                os.remove(f"{_dir}/content/result/screening/tmp.tab.fmt")
    
        print('Finished running foldseek screening')
####################################

    if SCREEN == "fatcat":
        files = subprocess.check_output("ls", cwd=f"{_dir}/content/input", shell=True).decode().split("\n")[:-1]

        for f in files:
            fatcat_tab_file = f"{_dir}/content/result/screening/{f}.tab.fmt"
            fatcat_command = [
                f'{_dir}/content/programs/FATCAT-dist/FATCATMain/FATCATSearch.pl',
                f,
                f"{_dir}/content/database/list_{DATABASE}.tab",
                "-b",
                "-i1",
                "./",
                "-i2",
                f"../database/{DATABASE}"
            ]
            fatcat_output = subprocess.check_output(fatcat_command).decode()

            sort_command = ["sort", "-k11nr"]
            head_command = ["head", "-n", str(HEADN)]
            format_command = [
                "perl",
                f"{_dir}/content/programs/remolog/scripts/format_result_FATCAT.pl",
                "-",
                f"{_dir}/content/programs/remolog/data/maxScore_fatcat.tab"
            ]

            sorted_output = subprocess.check_output(sort_command, input=fatcat_output.encode()).decode()
            head_output = subprocess.check_output(head_command, input=sorted_output.encode()).decode()
            formatted_output = subprocess.check_output(format_command, input=head_output.encode()).decode()

            with open(fatcat_tab_file, "w") as file:
                file.write(formatted_output)

        fmt_files = glob.glob(f"{_dir}/content/result/screening/*.fmt")
        with open(f"{_dir}/content/result/fatcat_formatted.tab", "w") as output_file:
            for fmt_file in fmt_files:
                with open(fmt_file, "r") as input_file:
                    output_file.write(input_file.read())

        print('Finished running fatcat screening')
#################################

    if SCREEN == "tmalign":
        files = subprocess.check_output("ls", cwd=f"{_dir}/content/input", shell=True).decode().split("\n")[:-1]
        
        for f in files:
            tab_file = f"{_dir}/content/result/screening/" + f + ".tab"
            subprocess.call("rm " + tab_file, shell=True)

            list_file = f"{_dir}/content/database/list_{DATABASE}.tab"
            database_files = subprocess.check_output("cat " + list_file, cwd=f"{_dir}/content/database", shell=True).decode().split("\n")[:-1]
            
            for l in database_files:
                tmalign_input_file = f"{_dir}/content/input/{f}"
                tmalign_database_file = f"{_dir}/content/database/{DATABASE}/{l}.pdb"###
                tmalign_output = subprocess.check_output([f"{_dir}/content/bin/TMalign", tmalign_input_file, tmalign_database_file]).decode()
                
                parser_cmd = ["perl", f"{_dir}/content/programs/remolog/scripts/parser_TMalign.pl", "-"]
                parser_output = subprocess.check_output(parser_cmd, input=tmalign_output.encode()).decode()
                
                with open(tab_file, "a") as file:
                    file.write(parser_output)
    
            # sort_cmd = "sort -k3nr " + tab_file + " | grep " + f + " | head -n {HEADN} > " + tab_file + ".fmt"
            # subprocess.call(sort_cmd, shell=True)
            sort_output = subprocess.check_output(["sort", "-k3nr", tab_file]).decode()
            grep_output = subprocess.check_output(["grep", f], input=sort_output.encode()).decode()
            head_output = subprocess.check_output(["head", "-n", str(HEADN)], input=grep_output.encode()).decode()
        
            with open(f"{tab_file}.fmt", "w") as fmt_file:
                lines = head_output.split("\n")
                for line in lines:
                    columns = line.split()
                    if len(columns) > 1:
                        columns[1] = os.path.splitext(columns[1])[0]  # Remover a extensão .pdb
                    fmt_file.write("\t".join(columns) + "\n")
            # with open(f"{tab_file}.fmt", "w") as fmt_file:
            #     lines = head_output.split("\n")
            #     for line in lines:
            #         columns = line.split()
            #         fmt_file.write("\t".join(columns) + "\n")

                    
        fmt_files = [file for file in os.listdir(f"{_dir}/content/result/screening") if file.endswith(".fmt")]
        with open(f"{_dir}/content/result/tmalign_formatted.tab", "w") as output_file:
            for fmt_file in fmt_files:
                with open(f"{_dir}/content/result/screening/{fmt_file}", "r") as input_file:
                    output_file.write(input_file.read())
  
        print('Finished running tmalign screening')
###################################        
    if SCREEN != "fatcat":
        fatcatFile = f'{_dir}/content/result/fatcat_formatted.tab'

        if os.path.isfile(fatcatFile):
            os.remove(fatcatFile)

        for f in os.listdir('.'):
            with open(f'{_dir}/content/result/screening/{f}.tab.fmt') as fatcatFileInputFile:
               for l in fatcatFileInputFile.readlines():
                    columns = l.split('\t')
                    if len(columns) > 1:
                        l = columns[1].strip()
                        l = l + '.pdb'
                    fatcatCommand = [
                        f'{_dir}/content/programs/FATCAT-dist/FATCATMain/FATCAT',
                        '-p1', f,
                        '-i1', '../input',
                        '-p2', l,
                        '-i2', f'../database/{DATABASE}',
                        '-b'
                    ]
                    fatcatProcess = subprocess.Popen(fatcatCommand, stdout=subprocess.PIPE)
                    fatcatOutput, _ = fatcatProcess.communicate()
                    
                    with open(f'{_dir}/content/result/tmpfatcatfile', 'a') as fatcatOutputFile:
                        fatcatOutputFile.write(fatcatOutput.decode())


                    formatCommand = [
                        'perl',
                        f'{_dir}/content/programs/remolog/scripts/format_result_FATCAT.pl',
                        '-',
                        f'{_dir}/content/programs/remolog/data/maxScore_fatcat.tab',
                    ]
                    formatProcess = subprocess.Popen(formatCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    formattedOutput, _ = formatProcess.communicate(input=fatcatOutput)

                    with open(fatcatFile, 'a') as fatcatOutputFile:
                        fatcatOutputFile.write(formattedOutput.decode())

        if os.path.isfile(f'{_dir}/content/result/tmpfatcatfile'):
            os.remove(f'{_dir}/content/result/tmpfatcatfile')
        
    
        print('Finished running FATCAT')
####################################
    if SCREEN != "tmalign":
        tmalignFile = f"{_dir}/content/result/tmalign_formatted.tab"

        if os.path.isfile(tmalignFile):
            os.remove(tmalignFile)

        for file in os.listdir(f"{_dir}/content/input"):
            tabFile = f"{_dir}/content/result/screening/{file}.tab.fmt"
            with open(tabFile) as tabFileInput:
                for line in tabFileInput:
                    l = line.split("\t")[1].strip()
                    l = l + ".pdb"
                    l_without_ext = os.path.splitext(l)[0]
                    tmalignCommand = [
                        f"{_dir}/content/bin/TMalign",
                        f"{_dir}/content/input/{file}",
                        f"{_dir}/content/database/{DATABASE}/{l}",
                    ]
                    tmalignProcess = subprocess.Popen(tmalignCommand, stdout=subprocess.PIPE)
                    tmalignOutput, _ = tmalignProcess.communicate()

                    parserCommand = [
                        "perl",
                        f"{_dir}/content/programs/remolog/scripts/parser_TMalign.pl",
                        "-",
                    ]
                    parserProcess = subprocess.Popen(
                        parserCommand,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                    )
                           
                    formattedOutput, _ = parserProcess.communicate(input=tmalignOutput)

                    formattedOutputLines = formattedOutput.decode().splitlines()
                    formattedOutputLines = [
                        line.replace(l, l_without_ext, 1) for line in formattedOutputLines
                    ]
                    formattedOutput = "\n".join(formattedOutputLines) + "\n"

                    with open(tmalignFile, "a") as tmalignOutputFile:
                        tmalignOutputFile.write(formattedOutput)

        print('Finished running tmalign')
####################################
        
    if SCREEN != "lovoalign":
        lovoalignFile = f'{_dir}/content/result/lovoalign_formatted.tab'
        tempLovoalignFile = f'{_dir}/content/result/tempLovoalignFile.tab'

        if os.path.isfile(lovoalignFile):
            os.remove(lovoalignFile)
        
        for f in os.listdir('.'):
            with open(f'{_dir}/content/result/screening/{f}.tab.fmt') as lovoalignInputFile:
                open(lovoalignFile, 'w').close()  # Limpar o arquivo lovoalignFile antes de começar o loop
            
                for l in lovoalignInputFile.readlines():
                    columns = l.split('\t')
                    if len(columns) > 1:
                        l = columns[1].strip()
                    lovoalignCommand = [
                        f'{_dir}/content/bin/lovoalign',
                        '-p1', f'{_dir}/content/input/{f}',
                        '-p2', f'{_dir}/content/database/{DATABASE}/{l}.pdb',
                    ]
                    lovoalignProcess = subprocess.Popen(lovoalignCommand, stdout=subprocess.PIPE)
                    lovoalignOutput, _ = lovoalignProcess.communicate()
        
                    with open(tempLovoalignFile, 'w') as lovoalignOutputFile:
                        lovoalignOutputFile.write(lovoalignOutput.decode())
        
                    parserCommand = [
                        'perl',
                        f'{_dir}/content/programs/remolog/scripts/parser_lovoalign.pl',
                        tempLovoalignFile,
                    ]
                    parserProcess = subprocess.Popen(parserCommand, stdout=subprocess.PIPE)
                    parserOutput, _ = parserProcess.communicate()
        
                    with open(lovoalignFile, 'a') as parserOutputFile:
                        lines = parserOutput.decode().split("\n")
                        for line in lines:
                            columns = line.split("\t")
                            if len(columns) > 1:
                                columns[1] = os.path.splitext(columns[1])[0]
                            formatted_line = "\t".join(columns)
                            if formatted_line.strip():
                                parserOutputFile.write(formatted_line + "\n")


            if os.path.isfile(tempLovoalignFile):
                os.remove(tempLovoalignFile)
            
        print('Finished running lovoalign')
####################################   
        
    result_dir = f"{_dir}/content/result"
    fatcat_file = f"{result_dir}/fatcat_formatted.tab"
    tmalign_file = f"{result_dir}/tmalign_formatted.tab"
    lovoalign_file = f"{result_dir}/lovoalign_formatted.tab"
    result_file = f"{result_dir}/result.tab"
   
    command1 = [
        "perl",
        f"{_dir}/content/programs/remolog/scripts/join_table.pl",
        fatcat_file,
        tmalign_file,
    ]
    processtest = subprocess.Popen(command1, stdout=subprocess.PIPE)
    tempCommand1File, _ = processtest.communicate()
                    
    with open(f'{_dir}/content/result/tempCommand1File', 'a') as fatcatOutputFile:
        fatcatOutputFile.write(tempCommand1File.decode())
        

    command2 = [
        "perl",
        f"{_dir}/content/programs/remolog/scripts/join_table.pl",
        f'{_dir}/content/result/tempCommand1File',
        lovoalign_file,
    ]

    processtest2 = subprocess.Popen(command2, stdout=subprocess.PIPE)
    tempCommand2File, _ = processtest2.communicate()
                
    with open(f'{_dir}/content/result/tempCommand2File', 'a') as fatcatOutputFile2:
        fatcatOutputFile2.write(tempCommand2File.decode())
    
    # Executar command3 usando o arquivo temporário como entrada
    command3 = [
        "perl",
        f"{_dir}/content/programs/remolog/scripts/add_scope_class.pl",
        f'{_dir}/content/result/tempCommand2File',
        ANNOT,
    ]

    # Redirecionar a saída para o arquivo result.tab
    with open(result_file, "w") as output_file:
        process3 = subprocess.Popen(
            command3, stdin=subprocess.PIPE, stdout=output_file, stderr=subprocess.PIPE
            )
        process3.wait()

    # Remover arquivos temporarios
    if os.path.isfile(f'{_dir}/content/result/tempCommand1File'):
        os.remove(f'{_dir}/content/result/tempCommand1File')
    if os.path.isfile(f'{_dir}/content/result/tempCommand2File'):
        os.remove(f'{_dir}/content/result/tempCommand2File')
    # Remover arquivos intermediários
    # if os.path.isfile(fatcatFile):
    #     os.remove(fatcatFile)
    # if os.path.isfile(tmalignFile):
    #     os.remove(tmalignFile)
    # if os.path.isfile(lovoalignFile):
    #     os.remove(lovoalignFile)
    
    print('Your task has been completed!')