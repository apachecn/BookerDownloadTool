import argparse
import sys
from . import __version__
from . import *

def main():
    parser = argparse.ArgumentParser(prog="BookerDownloadTool", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version=f"PYBP version: {__version__}")
    parser.set_defaults(func=lambda x: parser.print_help())
    subparsers = parser.add_subparsers()
    
    gh_book_parser = subparsers.add_parser("gh-book", help="download books from github")
    gh_book_parser.add_argument("url", help="SUMMARY.md url")
    gh_book_parser.add_argument("-t", "--threads", type=int, default=5, help="num of threads")
    gh_book_parser.add_argument("-p", "--proxy", help="proxy")
    gh_book_parser.add_argument("-a", "--article", default='article', help="article selector")
    gh_book_parser.set_defaults(func=dl_gh_book)
    
    bili_parser = subparsers.add_parser("bili", help="download bilibili video")
    bili_parser.add_argument("id", help="av or bv")
    bili_parser.add_argument("-a", "--audio", type=bool, default=False, help="whether to convert to audio")
    bili_parser.set_defaults(func=download_bili)

    bili_kw_parser = subparsers.add_parser("bili-kw", help="download bilibili video by kw")
    bili_kw_parser.add_argument("kw", help="keyword")
    bili_kw_parser.add_argument("-s", "--start", type=int, default=1, help="starting page")
    bili_kw_parser.add_argument("-e", "--end", type=int, default=10000000, help="ending page")
    bili_kw_parser.add_argument("-a", "--audio", type=bool, default=False, help="whether to convert to audio")
    bili_kw_parser.set_defaults(func=batch_kw_bili)
  
    bili_home_parser = subparsers.add_parser("bili-home", help="download bilibili video by user")
    bili_home_parser.add_argument("mid", help="user id")
    bili_home_parser.add_argument("-s", "--start", type=int, default=1, help="starting page")
    bili_home_parser.add_argument("-e", "--end", type=int, default=10000000, help="ending page")
    bili_home_parser.add_argument("-a", "--audio", type=bool, default=False, help="whether to convert to audio")
    bili_home_parser.set_defaults(func=batch_home_bili)
    
    args = parser.parse_args()
    args.func(args)
    
if __name__ == '__main__': main()