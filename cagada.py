import re

def extract_data_from_log(log_file):
    
    """Esta função lê o arquivo de log e usa expressões regulares para encontrar as bibliotecas
      que já estão instaladas, as que precisam ser instaladas, as que precisam ser desinstaladas e 
      as que foram desinstaladas com sucesso. Essas informações são retornadas em um dicionário.g"""
    
    with open(log_file) as f:
        log = f.read()
    file_paths = {
        "already_installed": re.findall(r"(?<=Requirement already satisfied: )\S+", log),
        "to_be_ignored": re.findall(r"(?<=ERROR: pip's dependency resolver does not).+(?=\n)", log),
        "uninstalled": re.findall(r"(?<=Successfully uninstalled )\S+", log),
        "to_be_uninstalled": re.findall(r".+(?=Successfully installed)", log)
    }
    return file_paths

def generate_uninstall_commands(file_paths):
    
    """esta função gera comandos para instalar as bibliotecas que precisam ser instaladas. Ele recebe 
    como entrada o dicionário retornado pela função extract_data_from_log()"""

    commands = []
    for file_path in file_paths["to_be_uninstalled"]:
        commands.append(f"pip uninstall -y {file_path}")
    return commands

def generate_install_commands(file_paths):
    """ esta função gera comandos para instalar as bibliotecas que precisam ser instaladas. Ele recebe 
    como entrada o dicionário retornado pela função extract_data_from_log()"""
    commands = []
    for file_path in file_paths["uninstalled"]:
        commands.append(f"pip install {file_path}")
    return commands

def generate_requirements_file(file_paths):
    """Gera um novo arquivo requirements.txt com as bibliotecas a serem mantidas"""
    with open("requirementsbacktodefuture.txt", "w") as f:
        for file_path in file_paths["already_installed"]:
            f.write(file_path + "\n")


def write_commands_to_file(output_file, uninstall_commands, install_commands):
    """
    Gera um arquivo com os comandos para desinstalar e reinstalar as bibliotecas.

    :param output_file: O nome do arquivo a ser gerado.
    :param uninstall_commands: A lista de comandos para desinstalar as bibliotecas.
    :param install_commands: A lista de comandos para reinstalar as bibliotecas.
    """
    with open(output_file, "w") as f:
        f.write("# Comandos para desinstalar bibliotecas\n")
        f.write("\n".join(uninstall_commands))
        f.write("\n\n")
        f.write("# Comandos para reinstalar bibliotecas\n")
        f.write("\n".join(install_commands))
        f.close()

def main():
    """ Esta é a função principal que chama todas as outras funções para executar 
    o script. Ele lê o arquivo de log, chama extract_data_from_log() para extrair 
    as informações relevantes, chama generate_install_commands() e generate_uninstall_commands() 
    para gerar os comandos necessários e chama write_commands_to_file()"""
    
    log_file = './logdacagada.txt'
    output_file = './solucao.py'
    try:
        # extrai as informações relevantes do arquivo de log
        already_installed, to_be_ignored, to_be_installed, to_be_uninstalled,  = extract_data_from_log(log_file)

        # gera os comandos necessários para instalar/desinstalar as bibliotecas
        install_commands = generate_install_commands(to_be_installed)
        uninstall_commands = generate_uninstall_commands(to_be_uninstalled, already_installed)
        # para serem ignorados
        print(f"ignorados {to_be_ignored}")
        # escreve os comandos gerados em um arquivo
        write_commands_to_file(output_file, install_commands + uninstall_commands)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == '__main__':
    main()