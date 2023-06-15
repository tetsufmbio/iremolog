import click
import os
import subprocess
#import shutil
#import glob

from get_dependencies import get_dependencies
from create_database import create_database
from running_protein_structure_alignment import running_proteins_structure
from fatcattest import fatcattest

# identifica a pasta atual do script
_dir = os.path.dirname(os.path.abspath(__file__))

# define a pasta atual como o diretório de trabalho padrão
os.chdir(_dir)

@click.command()
@click.option('--screening', prompt='Escolha uma opção para Screening software',
              type=click.Choice(['foldseek', 'tmalign', 'fatcat']),
              default='foldseek', 
              help='Software to be used to retrieve structurally similar proteins in SCOPe database.')

@click.option('--num_analyze', prompt='Escolha uma opção para most similar protein structures to be analyzed',
              type=int, default=200,
              help='Number of most similar protein structures to analyze.')

@click.option('--database', prompt='Escolha uma opção para Protein structure database to be used',
              type=click.Choice(['scope40', 'scope95']), default='scope40',
              help='Protein structure database to be used.')

@click.option('--job_name', prompt='Escolha o jobName',
              type=str, default='remolog_final_result',
              help='Prefix for the final output name.')


def main(screening, num_analyze, database, job_name):
    print(f'A opção escolhida foi {screening}')
    print(f"Number of protein structures to analyze: {num_analyze}")
    print(f'Protein structure database to be used: {database}')
    print(f'jobName to be used: {job_name}')

    os.environ['FATCAT'] = f'{_dir}/content/programs/FATCAT-dist'
    os.environ['PATH'] += f':{_dir}/content/programs/FATCAT-dist/FATCATMain'
    os.environ['HEADN'] = str(num_analyze)
    os.environ['SCREEN'] = screening
    os.environ['DATABASE'] = database
    annot = ''

    if (database == "scope40"):
        os.environ['ANNOT'] = f"{_dir}/content/programs/remolog/data/dir.cla.scope.2.08-stable_filtered40.txt"
        annot = os.environ['ANNOT']
    elif (database == "scope95"):
        os.environ['ANNOT'] = f"{_dir}/content/programs/remolog/data/dir.cla.scope.2.08-stable_filtered95.txt"
        annot = os.environ['ANNOT']
    if not os.path.exists('content'):
        os.makedirs('content')
        os.makedirs('content/input')

    subprocess.run(['bash', '-c', 'cd ./content/ && if [ ! -d bin ]; then mkdir bin; fi'])
    subprocess.run(['bash', '-c', 'cd ./content/ && if [ ! -d programs ]; then mkdir programs; fi'])
    subprocess.run(['bash', '-c', 'cd ./content/ && if [ ! -d view ]; then mkdir view; fi'])
    subprocess.run(['bash', '-c', 'cd ./content/ && if [ ! -d foldseek_data ]; then mkdir foldseek_data; fi'])

    get_dependencies(_dir)
    create_database(_dir, database)
    running_proteins_structure (_dir, screening, database, num_analyze, annot)
    # fatcattest(_dir, screening, database, num_analyze, annot)

if __name__ == '__main__':
    main()
