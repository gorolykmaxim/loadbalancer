import asyncssh


class CommandExecutionError(Exception):
    """Error, that occurs when executed command finishes with a non-0 exit code."""
    def __init__(self, code, stderr):
        """Constructor of the CommandExecutionError.

        Args:
            code (int): Exit code of the command.
            stderr (str): Error log of the command.

        """
        message = "Process exited with code {}. Error log:\n{}".format(code, stderr)
        super(CommandExecutionError, self).__init__(message)


class CommandExecutor(object):
    """A command executor, that executes commands remotely via SSH."""
    def __init__(self, username, password):
        """Constructor of the CommandExecutor.

        Args:
            username (str): Name of the SSH user.
            password (str): Password of the SSH user.

        Raises:
            Exception: If username or password were not specified.

        """
        if username is None:
            raise Exception("USERNAME parameter was not specified")
        if password is None:
            raise Exception("PASSWORD parameter was not specified")
        self.__username = username
        self.__password = password

    async def execute(self, host, command):
        """Execute specified command on the specified host and return the STDOUT of it.

        Note: awaitable method.

        Args:
            host (str): Remote host to execute command on.
            command (str): Command to execute.

        Returns:
            str: Output of the executed command.

        Raises:
            CommandExecutionError: If command exited with a non-0 exit code.

        """
        async with asyncssh.connect(host, username=self.__username, password=self.__password) as connection:
            result = await connection.run(command)
            if result.exit_status == 0:
                return result.stdout
            else:
                raise CommandExecutionError(result.exit_status, result.stderr)
