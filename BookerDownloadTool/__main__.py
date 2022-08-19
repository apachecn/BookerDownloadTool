import argparse
import sys
from . import __version__
from . import *

def main():
    parser = argparse.ArgumentParser(prog="BookerPubTool", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version=f"PYBP version: {__version__}")
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()
    
    docker_pub_parser = subparsers.add_parser("pub-docker", help="publish book to dockerhub")
    docker_pub_parser.add_argument("dir", help="dir")
    docker_pub_parser.set_defaults(func=publish_docker)

    pypi_pub_parser = subparsers.add_parser("pub-pypi", help="publish book to pypi")
    pypi_pub_parser.add_argument("dir", help="dir")
    pypi_pub_parser.set_defaults(func=publish_pypi)
    
    pypi_config_parser = subparsers.add_parser("conf-pypi", help="configure pypi token")
    pypi_config_parser.add_argument("token", help="token")
    pypi_config_parser.set_defaults(func=config_pypi)
    
    npm_pub_parser = subparsers.add_parser("pub-npm", help="publish book to npm")
    npm_pub_parser.add_argument("dir", help="dir")
    npm_pub_parser.set_defaults(func=publish_npm)
    
    npm_config_parser = subparsers.add_parser("conf-npm", help="configure npm token")
    npm_config_parser.add_argument("token", help="token")
    npm_config_parser.set_defaults(func=config_npm)
    
    ebook2site_parser = subparsers.add_parser("ebook2site", help="convert an ebook to a site")
    ebook2site_parser.add_argument("name", help="name")
    ebook2site_parser.add_argument("file", help="file")
    ebook2site_parser.add_argument("-d", "--dir", help="dir", default='.')
    ebook2site_parser.set_defaults(func=ebook2site)
    
    libgen_parser = subparsers.add_parser("libgen", help="upload to libgen")
    libgen_parser.add_argument("series", help="series")
    libgen_parser.add_argument("fname", help="file name")
    libgen_parser.add_argument("-t", "--threads", type=int, default=3, help="thread count")
    libgen_parser.add_argument("-p", "--proxy", help="proxy")
    libgen_parser.set_defaults(func=upload_libgen)
    
    args = parser.parse_args()
    args.func(args)
    
if __name__ == '__main__': main()