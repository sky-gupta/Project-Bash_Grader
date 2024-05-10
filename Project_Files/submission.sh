#!usr/bin/bash
################################fucntion declarations
function show_loading() {
    BAR_WIDTH=50   #length of the bar that we want
    percent=0  #initialize percentage
    while true; do
        echo -n -e "\r["

        # Calculate percentage completion
        if [ $percent -lt 100 ]; then
            percent=$((percent+10))  #increase the percent for progress bar
        else
            percent=100
        fi

        # Draw the background bar
        completed=$((percent * BAR_WIDTH / 100))
        remaining=$((BAR_WIDTH - completed))

        for ((i = 0; i < completed; i++)); do
            echo -n "="    #make this much bar appear completed
        done

        echo -n ">"

        for ((i = 0; i < remaining; i++)); do
            echo -n " " ##make remaining bar appear empty
        done

        echo -n "] Progress: $percent%"
        sleep 0.5  # Adjust the sleep duration as needed
    done
}


function combine {
    echo "Combining "
    t=0                 #variable to store if total was there or not
    if [ -f "main.csv" ]; then
        line=`head -1 main.csv`
        if grep -q "total" <<< "$line"; then            #to check if initially total was there in main.csv so as to update later
            t=1
        fi
        rm main.csv
        echo "Roll_Number,Name" > main.csv
    else
        echo "Roll_Number,Name" > main.csv      #if initially main.csv not present then make it with head
    fi

    for file in *.csv; do
        if [[ "$file" != "main.csv" && "$file" != ".aux_file" ]]; then   #search for all csv except main.csv(for comparing with)
            col=$(echo $file | sed -E 's/(.*).csv/\1/g')  #extract the file without extension
            sed -E -i "s/(^Roll_Number.*$)/\1,$col/g" main.csv  #to create more columns corresponding to each file
            num=`head -1 main.csv | tr ',' '\n' | wc -l` #to count how many fields
            `tail -n +2 $file > .aux_file`    #make an auxilliary file so as not to edit main.csv

            while read -r line; do
                roll_no=$(echo $line | cut -d ',' -f 1)  #extract roll_no,name and marks
                name=$(echo $line | cut -d ',' -f 2)
                marks=$(echo $line | cut -d ',' -f 3)

                    if grep -i -q $roll_no main.csv; then   #if roll_no already exists in main.csv 
                        mline=`grep -i $roll_no main.csv`
                        curr_num=`echo $mline | tr ',' '\n' | wc -l`
                        mline=${mline//[$'\n\r\t']/}    #remove carriage character from ending
                        newline="$mline"",""$marks"
                        newline=${newline//[$'\n\r\t']/}
                        if((curr_num==num-1)); then    #to ensure that it doesnt append multiple times
                            sed -E -i "s/$mline/$newline/g" main.csv
                        fi
                    else
                        s=""
                        for((i=1;i<=num-3;i++)); do # if roll_no does not exists then make a new row and append 'a' to all other csv files
                            s="$s"",a"
                        done
                        prev_num=`grep $roll_no main.csv | tr ',' '\n' | wc -l`
                        if((prev_num!=num)); then
                            nline=$roll_no,$name$s,$marks
                            nline=${nline//[$'\n\r\t']/}
                            echo $nline >> main.csv #otherwise make new line with new roll no , name and make empty field for rest csv file as a
                        fi
                    fi

            done < ".aux_file"
            rm .aux_file
            while read -r line; do  # for those roll_no in main.csv but not in current csv file 
                roll_no=$(echo $line | cut -d ',' -f 1)
                line=${line//[$'\n\r\t']/}
                curr_num=`echo $line | tr ',' '\n' | wc -l`  # for those roll no in main.csv not in '$file' append a
                if((curr_num==num-1)); then
                    newline="$line"",a"
                    sed -E -i "s/$line/$newline/g" main.csv
                fi
            done < "main.csv"
        fi
    done
    if(($t==1)); then  #if initially total was there then update that column
        total
    fi
}

function upload {
    file=$1 #variable for path to copy in
    `cp $file ./`
    return
}



function total {
    if grep -q "total" main.csv; then   #if already totalled then donot do that again
        echo "Total has already been done!"
    else
        awk -f total.awk main.csv > nmain.csv #awk file to find total
        cp nmain.csv main.csv
        rm nmain.csv
    fi
    return
}

function update {
    read -p "Please enter Student's Roll Number: " roll_no  #user input for various credentials
    read -p "Please enter Student's name: " n_name
    read -p "Please enter the exam name(case sensitive): " exam
    file="$exam"".csv"
    if [ ! -f $file ]; then   #if no such file is there then ask again
        echo "Invalid exam name!"
        read -p "Do you want to continue?(y/n)" bool   #to give more chances to user
        if [ "$bool" == "y" ]; then
            update   #recursively called the function
        else
            return
        fi
    else
        if grep -qi ^$roll_no.*$ $file; then   #find the student whose marks are to be updated
            read -p "Please enter updated marks: " new_marks
            o_name=$(grep -i ^$roll_no.*$ $file | cut -d ',' -f 2 )
            o_rollno=$(grep -i ^$roll_no.*$ $file | cut -d ',' -f 1 )
            n1=$(echo "$o_name" | sed -E 's/(.*)/\L\1/' | tr -d ' ' )  #first convert to lowercase and then trim all whitespaces
            n2=$(echo "$n_name" | sed -E 's/(.*)/\L\1/' | tr -d ' ' )
            if [[ "$n1" == "$n2" ]]; then    #if names are equal then only update
                echo "-------Updating marks---------"
                line=$o_rollno,$o_name,$new_marks
                line=${line//[$'\n\r\t']/}
                sed -E -i "s/^$roll_no.*$/$line/gI" $file
                combine
                echo "-------Updated successfully----"
                read -p "Do you want to continue?(y/n)" bool  #what if more cribs come to the TAs?
                if [ "$bool" == "y" ]; then
                    update
                else
                    return
                fi
            else
                echo "Names do not match for $roll_no!"   #otherwise throw an error
                read -p "Do you want to continue?(y/n)" bool
                if [ "$bool" == "y" ]; then
                    update
                else
                    return
                fi
            fi
        else
            read -p "Please enter updated marks: " new_marks
            echo "No such student exists for current exams!"  #if rollno & name don't match then ask again
            read -p "Do you want to continue?(y/n)" bool
            if [ "$bool" == "y" ]; then
                update
            else
                return
            fi
        fi
    fi
}

function git_init {
    path=$1
    if [ ! -d "$path" ]; then  #if initially its not there
        mkdir -p "$path"
        echo "Remote repository initialised"
    else
        
        echo "Remote repository already initialised"
    fi
}

function git_commit {
    repo=$1
    message=${@:2}   #get all the arguments from 2nd as message
    if [ ! -f $repo/.git_log ]; then
        touch $repo/.git_log  #if git_log not there make one
    fi
    touch .all_files
        num=$( grep "^[1-9].*$" $repo/.git_log | wc -l )
        if((num==0)); then
            echo "Nothing is commited till now!"   #if there is no commit id then tell the user that its your first commit
            echo "Your first commit has been made!"
        else
            hash_id=$( cat $repo/.git_log | tail -n 2 | head -n 1 | cut -d ',' -f 1 )  #if its there then take the latest commit id
            for file in $repo/$hash_id/*.csv; do
                o_file=`basename "$file"`
                if [ ! -f ./$o_file ]; then  #if some files are not here (means deleted and hence modified) append in .all_files for deletions
                    echo $file >> .all_files
                else
                    if cmp -s $file ./$o_file; then  #otherwise compare the two files and append correspondingly for modifications
                        continue
                    else
                        echo "$file" >> .all_files
                    fi
                fi
            done
            for nfile in ./*.csv; do  #similarly loop through current directory to know additions
                n_file=$(basename $nfile)
                if [ ! -f $repo/$hash_id/$n_file ]; then
                    echo $n_file >> .all_files
                fi
            done
        fi
    random_number=$(shuf -i 1000000000000000-9999999999999999 -n 1)  #generates random number of 16 digits
    mkdir $repo/$random_number
    cp -a ./*.csv $repo/$random_number  #copy the current version as commit to remote folder with commit id as name and corresponding message in git_log file
    echo "Commit made at: $(date)" >> $repo/.git_log
    echo "$random_number,\"$message\"" >> $repo/.git_log
    echo "===========================" >> $repo/.git_log
    if [ "$(stat -c %s ".all_files")" -gt 0 ]; then
        echo "The following files have been modified:"  #show the user about the modified files
        while read -r line; do
            echo $(basename $line)
        done < .all_files
    else
        echo "None of the file has been modified!" #if empty then show that no modifications
    fi
    rm .all_files  #delete it
}

function git_checkout {
    while read -r line; do   #get the remote address from .git_info
        repo=$line
    done < ".git_info"
    if [ "$1" == "m" ]; then   #if checkout is to be made by message (detect -m)
        message=${@:2}    #get the message from 2nd argument
        num=$(cat $repo/.git_log | grep "^[1-9].*,\"$message\"$" | cut -d ',' -f 1 | wc -l)   #search the corresponding commit id from .git_log file
        if [ $num -gt 1 ]; then   #if more than 1 ids with same message then throw conflicts and ask hash values
            read -p "Comflicts! Two or more commits have same messages.Do you want to try again with hash value?(y/n)" bool
            if [ "$bool" == "y" ]; then
                echo $(cat $repo/.git_log | grep "^[1-9].*,\"$message\"$") | sed -E 's/([^,]")/\1\n/g'   #suggest closest matching commit ids
                read -p "Enter corect commit-id:" hash
                git_checkout $hash  #recursively call the function with hash value as arg
            else
                exit 0
            fi
        elif [ $num -eq 0 ]; then   #if no such message then try with hash value
            read -p "There is no commit with this message.Do you want to try again with hash value?(y/n)" bool
            if [ "$bool" == "y" ]; then
                read -p "Enter corect commit-id:" hash
                git_checkout $hash    #recursively call the fucntion with hash value as arg
            else
                exit 0
            fi
        else
            hash_id=$(cat $repo/.git_log | grep "^[1-9].*,\"$message\"$" | cut -d ',' -f 1 )   #if find the correct one 
            rm -r ./*.csv                              #delete current version
            echo "==========checkout done successfully=============="
            cp $repo/$hash_id/*.csv .    #copy the old version
        fi
    else    #if checkout is made via hash value
        n_hash=$1 
        num=$(cat $repo/.git_log | grep "^$n_hash.*,\".*\"$" | cut -d ',' -f 1 | wc -l)   #get the all commit ids with this prefix
        if [ $num -gt 1 ]; then    #if many then throw conflicts 
            read -p "Comflicts! Two or more commits have same prefix.Do you want to try again with more correct hash value?(y/n)" bool
            if [ "$bool" == "y" ]; then
                echo $(cat $repo/.git_log | grep "^$n_hash.*,\".*\"$") | sed -E 's/([^,]")/\1\n/g'
                read -p "Enter corect commit-id:" n_hash
                git_checkout $n_hash
            else
                exit 0
            fi
        elif [ $num -eq 0 ]; then   #if doesnt exits then give more chance to user
            read -p "There is no commit with this prefix.Do you want to try again?(y/n)" bool
            if [ "$bool" == "y" ]; then
                read -p "Enter corect commit-id:" hash
                git_checkout $hash
            else
                exit 0
            fi
        else  #if present then do the same process as above of checkout
            hash_id=$(cat $repo/.git_log | grep "^$n_hash.*,\".*\"$" | cut -d ',' -f 1 )
            rm -r .*.csv
            echo "==========checkout done successfully=============="
            cp $repo/$hash_id/*.csv ./sample
        fi
    fi
}

######################################################CUSTOMIZATIONS###################################################

function analysis {   #see python file to understand its execution
    python3 analysis.py
}

function grading {
    total    #do totalling to get grades
    echo "Roll_Number,Name,Grades" > grades.txt   #make grades.txt and append header
    python3 abs.py   #see python file to understand its execution
}

function report {
    read -p "Enter Student's name: " name     #get the name of the student
    s_name=$(grep "$name" "main.csv" | cut -d ',' -f 2)
    if [ "$s_name" == "$name" ]; then   #if exact matched then 
        roll=$(grep -i "$name" "main.csv" | cut -d ',' -f 1)  #get the roll number
        if [ ! -f "grades.txt" ]; then    #if grading not done yet...do that and make a counter "found" to delete it later to restore the file system
            found=1
            grading
        fi
        if [ ! -f "result.tex" ]; then   #if tex file not there make it
            touch result.tex
        fi
        if grep -q "total" "main.csv"; then   #if totalling not done yet....do that
            echo -n ""
        else
            total
        fi
        python3 result.py $roll   #see the python file to understand it that takes roll number as argument
        pdflatex result.tex  > /dev/null   #execute the tex and send the commandline output to dev/null
        evince result.pdf     #open the pdf file 
        if((found==1)); then
            rm grades.txt    #if initially not there...then delete it
        fi
    else
        closest_match=$(python3 closest.py $name)   #if exactly not matched then find its closest match...see the python file to understand
        read -p "Do you mean by $closest_match (y/n)?" bool
        if [ "$bool" == "y" ]; then
            name=$closest_match
            net=$(grep "$closest_match" "main.csv" | cut -d ',' -f 1 | wc -l)   #find the number of matches
            if((net==1)); then
                roll=$(grep "$closest_match" "main.csv" | cut -d ',' -f 1)
                if [ ! -f "grades.txt" ]; then
                    found=1
                    grading
                fi
                if [ ! -f "result.tex" ]; then
                    touch result.tex
                fi
                if grep -q "total" "main.csv"; then
                    echo -n ""
                else
                    total
                fi
                python3 result.py $roll
                pdflatex result.tex > /dev/null
                evince result.pdf
                if((found==1)); then
                    rm grades.txt
                fi
            else    #if many such matches then ask for roll number
                echo "Sorry there are $net students with \"$closest_match\" as there name!"
                read -p "Please enter Roll number: " roll
                if [ ! -f "grades.txt" ]; then
                    found=1
                    grading
                fi
                if [ ! -f "result.tex" ]; then
                    touch result.tex
                fi
                if grep -q "total" "main.csv"; then
                    echo -n ""
                else
                    total
                fi
                if grep -q "total" "main.csv"; then
                    echo -n ""
                else
                    total
                fi
                python3 result.py $roll
                pdflatex result.tex > /dev/null
                evince result.pdf
                if((found==1)); then
                    rm grades.txt
                fi
            fi
        elif [ "$bool" == "n" ]; then
            read -p "Enter the roll number: " roll
            python3 result.py $roll
            pdflatex result.tex > /dev/null
            evince result.pdf
        else
            echo "Invalid command!"
            exit 0
        fi
    fi
}

function search {
    read -p "Do you have name or roll number?(1/2)" bool   #ask the user for roll number or name
    if [ "$bool" == "1" ]; then
        read -p "Enter Student's name: " name     #ask the name
        s_name=$(grep "$name" "main.csv" | cut -d ',' -f 2)
        if [ "$s_name" == "$name" ]; then
            roll=$(grep -i "$name" "main.csv" | cut -d ',' -f 1)
            python3 search.py $roll
        else
            closest_match=$(python3 closest.py $name)
            read -p "Do you mean by $closest_match (y/n)?" bool
            if [ "$bool" == "y" ]; then
                name=$closest_match
                net=$(grep "$closest_match" "main.csv" | cut -d ',' -f 1 | wc -l)
                if((net==1)); then
                    roll=$(grep "$closest_match" "main.csv" | cut -d ',' -f 1)
                    python3 search.py $roll
                else
                    echo "Sorry there are $net students with \"$closest_match\" as there name!"
                    read -p "Please enter Roll number: " roll
                    python3 search.py $roll
                fi
            elif [ "$bool" == "n" ]; then
                read -p "Enter the roll number: " roll
                c=$(grep -i $roll "main.csv" | cut -d ',' -f 1 | wc -l)
                if((c==1)); then
                    python3 search.py $roll
                else
                    echo "This student doesn't exist!"
                    exit 0
                fi
            else
                echo "Invalid command!"
                exit 0
            fi
        fi
    elif [ "$bool" == "2" ]; then
        read -p "Enter the roll number: " roll
        c=$(grep -i $roll "main.csv" | cut -d ',' -f 1 | wc -l)
        if((c==1)); then
            python3 search.py $roll
        else
            echo "This student doesn't exist!"
            exit 0
        fi
    else
        echo "Invalid command!"
        exit 0
    fi
}

function general {
    python3 general_report.py   #see python file to understand
    pdflatex result.tex > /dev/null
    evince result.pdf
}

##################################to check if any command is there or not
if [ $# -eq 0 ]; then 
    echo "Invalid usage"
    exit 1
else
    com=$1 #variable declaration for command
fi


##################################to call functions on the basis of command line args
if [ "$com" == "combine" ]; then
    show_loading &
    loading_pid=$!
    combine
    kill $loading_pid >/dev/null 2>&1
    echo -e "\nCompleted."


elif [ "$com" == "upload" ]; then
    if [ $# -eq 2 ]; then
        upload $2
    else
        echo "Wrong usage {bash submission.sh upload <path>}"
    fi

elif [ "$com" == "total" ]; then
    total

elif [ "$com" == "update" ]; then
    update

elif [ "$com" == "git_init" ]; then
    if [ $# -eq 2 ]; then
        echo "$2" > .git_info
        git_init $2
    else
        echo "Wrong usage {bash submission.sh git_init <path>}"
    fi

elif [ "$com" == "git_commit" ]; then
    pattern=".*$"
    if [ ! -f .git_info ]; then
        touch .git_info
    fi
    while read -r line; do
        repo_path=$line
    done < ".git_info"
    if [ $# -eq 3 ] && [ "$2" == "-m" ] && [[ "${@:3}" =~ $pattern ]]; then
        if [[ "$repo_path" == "" ]]; then
            echo "ERROR: Remote repository not initialised"
            exit 1
        else
            git_commit $repo_path ${@:3}
        fi
    else
        echo "No commit message found!"
        echo "Usage: bash submission.sh git_commit -m \"message\""
    fi

elif [ "$com" == "git_checkout" ]; then
    pattern=".*$"
    if [ $# -eq 3 ] && [ "$2" == "-m" ] && [[ "${@:3}" =~ $pattern ]]; then
        git_checkout m ${@:3}
    elif [ $# -q 2 ] && [[ "$2" =~ "^[1-9]{1,}$" ]]; then
        git_checkout $2
    else
        echo "ERROR : Invalid usage: bash submission.sh git_checkout -m \"message\" or bash submission.sh git_checkout <Hash_Value>!"
    fi
elif [ "$com" == "analysis" ]; then
    analysis
elif [ "$com" == "grading" ]; then
    grading
elif [ "$com" == "report" ]; then
    report
    # rm *.png
elif [ "$com" == "search" ]; then
    search
elif [ "$com" == "general_report" ]; then
    general
fi