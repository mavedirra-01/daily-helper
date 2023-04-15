from click_shell import shell
import click
import click_completion
import os
import webbrowser
# import signal
import paramiko

g = "\033[32m[+]\033[0m"
r = "\033[91m[-]\033[0m"
bold = '\033[1m'
b = '\033[94m[-->]\033[0m'
y = '\033[93m[!]\033[0m'
rc = '\033[0m'

click_completion.init()

@shell(prompt='[Daily-Helper]>>> ', intro='Type "help" for options')

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
    drone = host
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
@click.option('--project-dir', default='C:\\Users\\wanda\\Documents\\Pentests', help='Main directory path')
def project_setup(project_name, project_dir):
    project_directory = os.path.join(project_dir, project_name)
    os.makedirs(os.path.join(project_directory, 'Docs'))
    os.makedirs(os.path.join(project_directory, 'Scans'))
    os.makedirs(os.path.join(project_directory, 'Report'))
    os.makedirs(os.path.join(project_directory, 'Screenshots'))
    file_path = os.path.join(project_directory, 'exec_summary.txt')
    with open(file_path, 'w') as f:
        f.write('exec summary')
    os.listdir(project_directory)
    click.echo('Directories created successfully!')


@main.command()
@click.option('--evidence', default='C:\\Users\\bsi553\\Documents\\Pentests\\core-helper\\evidence', help='Main directory path')
@click.option('--client', prompt='Enter client name', help='Name of the project', required=True, type=click.Path())
def move_evidence(evidence, client):
    new_file_path = os.path.join('C:\\Users\\wanda\\Documents\\Pentests', client, "evidence")
    os.rename(evidence, new_file_path)
    click.echo(f"Moved {evidence} to {new_file_path}")
    

@main.command()
@click.option('-c', '--client', required=True)
@click.option('-s', '--scope', required=True)
@click.option('-r', '--report-id', required=True)
@click.option('-d', '--file-path', required=True)
def nessus2plextrac(client, scope, report_id, file_path):
    script = r"C:\Users\bsi553\Desktop\reporting-toolset\Nessus2Plextrac.py"
    username = "-u "
    password = "-p FIXME"
    exec(open(script).read(), {'-c', client, '-s', scope, '-r', report_id, '-d', file_path, username, password})

if __name__ == '__main__':
    main()
