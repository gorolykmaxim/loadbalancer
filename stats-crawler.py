import asyncio

from statscrawler import StatsCrawler

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(StatsCrawler().main())
