import re
enum_dict = {
                "CONTROLLERFLAG"    : True,
                "NETWORKFLAG"       : False,
                "CAMERAFLAG"        : False,
                "MQTTSERVER"        : "",
                "MQTTPATH"          : "" 
}

def parse_argv(sys):
    # CLI Options
    if(len(sys.argv) > 1):
        if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            print("Useage:")
            print("karlos [options]\n")

            print("Available Options:")
            print("-n <subscriber-ip>             | -n <local>        : sets the ip address of the pi subscriber    <default: runs on local>")
            print("--network <subscriber-ip>      | --network <local> : sets the ip address of the pi subscriber    <default: runs on local>")
            print("-p <mqtt-path>                                     : sets the mqtt path of the subscriber")
            print("-path <mqtt-path>                                  : sets the mqtt path of the subscriber")
            print("-s <controller>                | -s <pose>         : sets the control                            <default: runs with controller>")
            print("-start <controller>            | -start <pose>     : sets the control                            <default: runs with controller>")
            print("-c                                                 : turns on the pi's camera                    <default: runs without camera>")
            print("-rf /path/to/file                                  : reads config data from a file")
            print("-readfile /path/to/file                            : reads config data from a file")
            return

        if(sys.argv.count('-n') == 1 or sys.argv.count('--network') == 1):
            ipexp = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
            try:
                arg_index = sys.argv.index('-n') 
            except:
                arg_index = sys.argv.index('--network') 
            try:
                enum_dict["NETWORKFLAG"] = True if ( sys.argv[arg_index + 1] != 'local' and re.search(ipexp, sys.argv[arg_index + 1])) else False
                enum_dict["MQTTSERVER"] = sys.argv[arg_index + 1]
                print("your subscriber ip has been set to:", (sys.argv[arg_index + 1]))
            except:
                print("Error: No input has been given for the flag '-n'")

        if(sys.argv.count('-p') == 1 or sys.argv.count('--path') == 1):
            try:
                arg_index = sys.argv.index('-p') 
            except:
                arg_index = sys.argv.index('--path') 
            try:
                enum_dict["MQTTPATH"] = sys.argv[arg_index + 1]
                print("MQTT PATH has been set to:", (sys.argv[arg_index + 1]))    
            except:
                print("Error: No input has been given for the flag '-p'")

        if(sys.argv.count('-s') == 1 or sys.argv.count('--start') == 1):
            try:
                arg_index = sys.argv.index('-s') 
            except:
                arg_index = sys.argv.index('--start') 
            try:
                enum_dict["CONTROLLERFLAG"] = sys.argv[arg_index + 1] == 'controller'
                print("your default control has been set to:", (sys.argv[arg_index + 1]))    
            except:
                print("Error: No input has been given for the flag '-s'")

        if(sys.argv.count('-c') == 1 or sys.argv.count('--camera') == 1):
            try:
                arg_index = sys.argv.index('-c') 
            except:
                arg_index = sys.argv.index('--camera') 

            enum_dict["CAMERAFLAG"] = True
            print("Camera has been set to: True")
        
        if(sys.argv.count('-rf') == 1 or sys.argv.count('-readfile')):
            try:
                arg_index = sys.argv.index('-rf') 
            except:
                arg_index = sys.argv.index('--readfile') 
            try:
                with open(sys.argv[arg_index + 1]) as config:
                    data = config.read().strip().split('\n')
                    data = [i.split(" = ") for i in data]
                    data = {data[i][0]: data[i][1] for i in range(len(data))}
                    config.close()
                return data
            except:
                print("Error opening config file: switching to defaults")
        
        return enum_dict