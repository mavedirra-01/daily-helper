from click_shell import shell
import click
import os
import webbrowser
import paramiko

g = "\033[32m[+]\033[0m"
r = "\033[91m[-]\033[0m"
bold = '\033[1m'
b = '\033[94m[-->]\033[0m'
y = '\033[93m[!]\033[0m'
rc = '\033[0m'

@shell(prompt='>>> ', intro='Type "help" for options')
def main():
    pass


@main.command()
@click.option('--host', prompt='Enter the hostname or IP address of the remote machine', help='Hostname or IP address of the remote machine')
@click.option('--username', prompt='Enter your username on the remote machine', help='Your username on the remote machine')
@click.option('--password', prompt=True, hide_input=True, help='Your password on the remote machine')
@click.option('--output', prompt='Enter the path of the output file', default=os.getcwd(), help='The path of the output file')
@click.option('--targetfile', prompt='Enter the path of the target file', default="up.txt", help='The path of the target file to be used as input for nmap')
def alive_hosts(host, username, password, output, targetfile):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    drone = host + '.kevlar.bulletproofsi.net'
    try:
        ssh.connect(hostname=drone, username=username, password=password)
    except Exception as e:
        click.echo(f"Error connecting to {drone}: {e}")
        return

    cmd = f"nmap -n -sn -iL {targetfile} --excludefile -oG - | awk '/Up\$/{{print $2}}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().decode('utf-8')

    with open(output, 'w') as f:
        f.write(result)
    click.echo(f"Output saved to {output}")
    try:
        start_nessus = "sudo systemctl start nessusd"
        ssh.exec_command(start_nessus)
    except Exception as e:
        click.echo(f"Error starting nessus : {e}")
        return
    ssh.close()


@main.command()
@click.option('--project-name', prompt='Enter client name', help='Name of the project')
@click.option('--project-dir', default='C:\\Users\\bsi553\\Documents\\Pentests', help='Main directory path')
def project_setup(project_name, project_dir):
    project_directory = os.path.join(project_dir, project_name)
    os.makedirs(os.path.join(project_directory, 'Docs'))
    os.makedirs(os.path.join(project_directory, 'Scans'))
    os.makedirs(os.path.join(project_directory, 'Report'))
    os.makedirs(os.path.join(project_directory, 'Screenshots'))
    file_path = os.path.join(project_directory, 'nmap.txt')
    with open(file_path, 'w') as f:
        f.write('nmap -n ')
    click.echo('Directories created successfully!')


links = [
    'https://www.google.com',
    'https://www.github.com',
    'https://www.linkedin.com'
]

@main.command()
def open_link():
    click.echo('Available links:')
    for i, link in enumerate(links):
        click.echo(f'{i+1}. {link}')

    while True:
        selection = click.prompt('Select a link to open (0 to quit)', type=int, default=1, show_default=True, prompt_suffix=': ')
        if selection == 0:
            return
        elif selection < 1 or selection > len(links):
            click.echo('Invalid selection')
        else:
            link = links[selection-1]
            webbrowser.open_new_tab(link)
            click.echo(f'Opened {link} in Firefox')
            return

@main.command()
@click.option('-c', '--client', required=True)
@click.option('-s', '--scope', required=True)
@click.option('-r', '--report-id', required=True)
@click.option('-d', '--file-path', required=True)
def nessus2plextrac(client, scope, report_id, file_path):
    script = r"C:\Users\bsi553\Desktop\reporting-toolset\Nessus2Plextrac.py"
    username = "-u mavedirra"
    password = "-p FIXME"
    exec(open(script).read(), {'-c', client, '-s', scope, '-r', report_id, '-d', file_path, username, password})

if __name__ == '__main__':
    main()
