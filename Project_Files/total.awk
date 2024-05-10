BEGIN{
    FS=",";
}
{
    if(NR==1){
        print $0 FS "total"
    }
    else{
            sum=0
            for(i=2;i<=NF;i++){
                sum=sum+$i
            }
            print $0 FS sum 
        }
}