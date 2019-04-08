from textwrap import dedent

from click.testing import CliRunner

from neuromation.cli.utils import DeprecatedGroup, MainGroup, command, group


def test_print():
    @group()
    def sub_command():
        pass

    @command()
    def plain_cmd():
        pass

    @group(cls=MainGroup)
    def main():
        pass

    main.add_command(sub_command)
    main.add_command(plain_cmd)

    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS] COMMAND [ARGS]...

        Commands:
          sub-command

        Command Shortcuts:
          plain-cmd

        Use "neuro <command> --help" for more information about a given command.
        Use "neuro --options" for a list of global command-line options (applies to all
        commands).
    """
    )


def test_print_use_group_helpers():
    @group(cls=MainGroup)
    def main():
        pass

    @main.group()
    def sub_command():
        pass

    @main.command()
    def plain_cmd():
        pass

    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS] COMMAND [ARGS]...

        Commands:
          sub-command

        Command Shortcuts:
          plain-cmd

        Use "neuro <command> --help" for more information about a given command.
        Use "neuro --options" for a list of global command-line options (applies to all
        commands).
    """
    )


def test_print_hidden():
    @group()
    def sub_command():
        pass

    @command(hidden=True)
    def plain_cmd():
        pass

    @group()
    def main():
        pass

    main.add_command(sub_command)
    main.add_command(plain_cmd)

    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS] COMMAND [ARGS]...

        Commands:
          sub-command
    """
    )


def test_print_deprecated_group():
    @group()
    def sub_command():
        """
        Sub-command.
        """

    @group()
    def main():
        pass

    main.add_command(sub_command)
    main.add_command(DeprecatedGroup(sub_command, name="alias"))

    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS] COMMAND [ARGS]...

        Commands:
          sub-command  Sub-command
          alias        Alias for sub-command
    """
    )


def test_print_deprecated_group_content():
    @group()
    def sub_command():
        """
        Sub-command.
        """

    @sub_command.command()
    def cmd():
        """Command.

        Detailed description is here.
        """

    @group(cls=MainGroup)
    def main():
        pass

    main.add_command(sub_command)
    main.add_command(DeprecatedGroup(sub_command, name="alias"))

    runner = CliRunner()
    result = runner.invoke(main, ["alias"])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main alias [OPTIONS] COMMAND [ARGS]...

          Alias for sub-command (DEPRECATED)

        Commands:
          cmd  Command
    """
    )


def test_print_deprecated_no_help():
    @command(deprecated=True)
    def main():
        pass

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS]

           (DEPRECATED)

        Options:
          --help  Show this message and exit.
    """
    )


def test_print_deprecated_with_help():
    @command(deprecated=True)
    def main():
        """Main help."""

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS]

          Main help. (DEPRECATED)

        Options:
          --help  Show this message and exit.
    """
    )


def test_print_help_with_examples():
    @command()
    def main():
        """
        Main help.

        Examples:

        # comment
        example

        """

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert result.output == dedent(
        """\
        Usage: main [OPTIONS]

          Main help.

        Examples:
          # comment
          example

        Options:
          --help  Show this message and exit.
    """
    )