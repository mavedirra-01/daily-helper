#!/bin/bash

function alive_hosts () {
    read -p "Enter the hostname or IP address of the remote machine: " host
    read -p "Enter your username on the remote machine: " username
    read -s -p "Enter your password on the remote machine: " password
    echo
    read -p "Enter the path of the output file (default is PWD/up.txt): " output
    read -p "Enter the path of the target file (default is targets.txt): " targetfile
    read -p "Enter the path of the exclude file (default is exclude.txt): " excludefile
    targetfile=${targetfile:-targets.txt}
    output=(${output:-up.txt})
    output=(${excludefile:-exclude.txt})
    sshpass -p $password ssh $username@$host "nmap -n -sn -iL $targetfile --excludefile $excludefile -oG - | awk '/Up\$/{print \$2}'" > $output
    echo "Output saved to $output"
    sshpass -p $password ssh $username@$host "sudo systemctl start nessusd"
}

function project_setup () {
    read -p "Enter client name: " project_name
    read -p "Enter main directory path (default is /mnt/c/Users/bsi553/Documents/Pentests): " project_dir
    project_dir=${project_dir:-/mnt/c/Users/bsi553/Documents/Pentests}
    project_directory="$project_dir/$project_name"
    mkdir -p "$project_directory/Docs"
    mkdir -p "$project_directory/Scans"
    mkdir -p "$project_directory/Report"
    mkdir -p "$project_directory/Screenshots"
    echo 'exec summary' > "$project_directory/exec_summary.txt"
    ls "$project_directory"
    echo "Directories created successfully!"
}

function move_evidence () {
    read -p "Enter client name: " client
    read -p "Enter main directory path (default is /mnt/c/Users/bsi553/Documents/Pentests/assessment-toolkit/Nessus-Helper/evidence): " evidence
    evidence=${evidence:-/mnt/c/Users/bsi553/Documents/Pentests/assessment-toolkit/Nessus-Helper/evidence}
    new_file_path="/mnt/c/Users/bsi553/Documents/Pentests/$client/evidence"
    mv "$evidence" "$new_file_path"
    echo "Moved $evidence to $new_file_path"
}

function nessus2plextrac () {
    read -p "Enter client name: " client
    read -p "Enter scope: " scope
    read -p "Enter report ID: " report_id
    read -p "Enter file path: " file_path
    script="/mnt/c/Users/bsi553/Desktop/reporting-toolset/Nessus2Plextrac.py"
    username="-u "
    password="-p FIXME"
    python3 $script -c $client -s $scope -r $report_id -d $file_path $username $password
}

PS3="[Daily-Helper]>>> "
options=("Alive Hosts" "Project Setup" "Move Evidence" "Nessus2Plextrac" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Alive Hosts")
            alive_hosts
            ;;
        "Project Setup")
            project_setup
            ;;
        "Move Evidence")
            move_evidence
            ;;
        "Nessus2Plextrac")
            nessus2plextrac
            ;;
        "Quit")
            break
            ;;
        *) echo "Invalid option $REPLY";;
    esac
done
