from AutoDD_Rev2.AutoDD import *
import argparse
import logging

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='AutoDD Optional Parameters')

    parser.add_argument('--interval', nargs='?', const=24, type=int, default=24,
                    help='Choose a time interval in hours to filter the results, default is 24 hours')

    parser.add_argument('--min', nargs='?', const=10, type=int, default=10,
                    help='Filter out results that have less than the min score, default is 10')

    parser.add_argument('--yahoo', default=False, action='store_true',
                    help='Using this parameter shows yahoo finance information on the ticker, makes the script run slower!')

    parser.add_argument('--sub', nargs='?', const='pennystocks', type=str, default='pennystocks',
                    help='Choose a different subreddit to search for tickers in, default is pennystocks')

    parser.add_argument('--sort', nargs='?', const=1, type=int, default=1,
                    help='Sort the results table by descending order of score, 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score, 5 = sort by # of rocket emojis')

    parser.add_argument('--allsub', default=False, action='store_true',
                    help='Using this parameter searchs from one subreddit only, default subreddit is r/pennystocks.')

    parser.add_argument('--csv', default=False, action='store_true',
                    help='Using this parameter produces a table_records.csv file, rather than a .txt file')

    parser.add_argument('--filename', nargs='?', const='table_records', type=str, default='table_records',
                    help='Change the file name from table_records to whatever you wish')

    args = parser.parse_args()

    print("Getting submissions...")
    # call reddit api to get results
    results_from_api = get_submission(args.interval/2, args.sub)  

    print("Searching for tickers...")
    current_tbl, current_rockets = get_freq_list(results_from_api[0])
    prev_tbl, prev_rockets = get_freq_list(results_from_api[1])

    print("Populating results...")
    results_tbl = combine_tbl(current_tbl, prev_tbl)

    results_tbl = filter_tbl(results_tbl, args.min)

    print("Counting rockets...")
    results_tbl = append_rocket_tbl(results_tbl, current_rockets, prev_rockets)

    if args.allsub:
        print("Searching other subreddits...")
        for api_result in results_from_api[2:]:
            results_tbl = additional_filter(results_tbl, api_result)

    if args.sort == 1:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][0], reverse=True)
    elif args.sort == 2:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][1], reverse=True)
    elif args.sort == 3:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][2], reverse=True)
    elif args.sort == 4:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][3], reverse=True)
    elif args.sort == 5:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][4], reverse=True)

    print("Getting quick stats...")
    results_tbl = getQuickStats(results_tbl)

    if args.yahoo:
        print("Getting yahoo finance information...")
        results_tbl = getTickerInfo(results_tbl)

    args.csv = True
    print_tbl(results_tbl, args.filename, args.allsub, args.yahoo, args.csv)

if __name__ == '__main__':
    main()