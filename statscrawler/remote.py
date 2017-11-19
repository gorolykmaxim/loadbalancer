import asyncssh


class CommandExecutionError(Exception):

    def __init__(self, code, stderr):
        message = "Process exited with code {}. Error log:\n{}".format(code, stderr)
        super(CommandExecutionError, self).__init__(message)


class CommandExecutor(object):

    def __init__(self, username, password):
        if username is None:
            raise Exception("USERNAME parameter was not specified")
        if password is None:
            raise Exception("PASSWORD parameter was not specified")
        self.__username = username
        self.__password = password

    async def execute(self, host, command):
        async with asyncssh.connect(host, username=self.__username, password=self.__password) as connection:
            result = await connection.run(command)
            if result.exit_status == 0:
                return result.stdout
            else:
                raise CommandExecutionError(result.exit_status, result.stderr)