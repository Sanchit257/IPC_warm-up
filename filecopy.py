import sys
import os


def main():
    #checks correct # of arguments
    if len(sys.argv) != 3:
        print("Error: 2 arguments only")
        sys.exit(1)
    #assign arguements to vars
    sfile = sys.argv[1]
    dfile = sys.argv[2]

    #checks if source file even exists
    if not os.path.exists(sfile):
        print(f"Error: '{sfile}' does not exist.")
        sys.exit(1)
    if not os.path.exists(dfile):
        print(f"Error: '{dfile}' does not exist.")
        sys.exit(1)

    read_pipe, write_pipe = os.pipe() #creates pipes for reading and writing
    child = os.fork() #creates child process
    #checks if fork failed. if so, exits and closes pipes
    if child < 0: 
        print("Error: No child exists/Fork process failed.")
        os.close(read_pipe)
        os.close(write_pipe)
        sys.exit(1)

    #code that executes in child process
    elif child == 0:
        os.close(write_pipe)     #close the write end of the pipe
        destination = open(dfile, 'w')  #opens the destination file

        #reads all data from pipe and writes to destination
        with os.fdopen(read_pipe, 'r') as pipe_read:
            destination.write(pipe_read.read())
        destination.close()#closes file
        sys.exit(0)

    else:#parent executes
        #closes read pipe
        os.close(read_pipe)

        #opens source file for reading
        source = open(sfile, 'r')

        #reads source file and writes to pipe
        with os.fdopen(write_pipe, 'w') as pipe_write:
            pipe_write.write(source.read())
        source.close()

        #waits for child process to finish so child doenst become a zombie process
        _,status = os.waitpid(child, 0)
        #checks if child exited 
        if os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0:
            print(f"File successfully copied from {sfile} to {dfile}.")
        else:
            print("A child process encountered an error during file copy.")
            sys.exit(1)

if __name__ == "__main__":
    main()