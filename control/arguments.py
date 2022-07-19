"""Builds the command line interface.

Exports a function to build the command line interface.

Functions:
    build_argparse()
"""

import argparse

from version import __version__, tf_version


def build_argparse() -> argparse.ArgumentParser:
    """Build the argparser.

    Builds the command line interface providing options for fade_dca, recall_scene, and set_mute_master.

    Returns:
        An instance of the argparse.ArgumentParser class
    """
    # Create argparser
    parser = argparse.ArgumentParser(
        prog="yamaha-desk-control",
        description="control various functions of yamaha series consoles.",
        epilog=f"these scripts have been tested against a yamaha tf-rack running v{tf_version}",
    )

    # version
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="returns the version number",
        version=f"%(prog)s {__version__}",
    )

    # Build Subparsers
    subparsers = parser.add_subparsers(help="available commmands")

    # fade_dca
    parser_fade_dca = subparsers.add_parser(
        "fade_dca", help="fade a selected dca to a target value over a given time"
    )

    # DCA number
    parser_fade_dca.add_argument(
        "-d",
        "--dca",
        metavar="<dca>",
        type=int,
        required=True,
        help="the dca to fade (1–16)",
        choices=range(1, 17),
    )

    # IP address
    parser_fade_dca.add_argument(
        "-i",
        "--ip",
        metavar="<ip address>",
        required=True,
        help="the console ip address",
    )

    # Target level
    parser_fade_dca.add_argument(
        "-l",
        "--level",
        metavar="<level>",
        type=int,
        required=True,
        help="the target level",
    )

    # Duration
    parser_fade_dca.add_argument(
        "-t",
        "--time",
        metavar="<duration>",
        type=float,
        required=True,
        help="the fade duration",
    )

    # recall_scene
    parser_recall_scene = subparsers.add_parser(
        "recall_scene", help="recall a scene. tf-series only."
    )

    # Bank letter
    parser_recall_scene.add_argument(
        "-b",
        "--bank",
        metavar="<bank>",
        type=str,
        default="a",
        help="the scene bank (a, b)",
        choices=["a", "b"],
    )

    # IP address
    parser_recall_scene.add_argument(
        "-i",
        "--ip",
        metavar="<ip address>",
        required=True,
        help="the console ip address",
    )

    # Scene number
    parser_recall_scene.add_argument(
        "-s",
        "--scene",
        metavar="<scene>",
        type=int,
        required=True,
        help="the scene to recall (0–100)",
        choices=range(0, 100),
    )

    # set_mute_master
    parser_set_mute_master = subparsers.add_parser(
        "set_mute_master", help="sets the input and fx mute masters. tf-series only."
    )

    # IP address
    parser_set_mute_master.add_argument(
        "-i",
        "--ip",
        metavar="<ip address>",
        required=True,
        help="the console ip address",
    )

    # Master
    parser_set_mute_master.add_argument(
        "-m",
        "--master",
        metavar="<master>",
        type=str,
        default="input",
        help="the mute master to be set (input, fx)",
        choices=["input", "fx"],
    )

    # State
    parser_set_mute_master.add_argument(
        "-s",
        "--state",
        metavar="<state>",
        type=str,
        required=True,
        help="the state to set the mute master to (on, off)",
        choices=["on", "off"],
    )

    return parser
