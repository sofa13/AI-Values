import sys
import multiprocessing as mp
import time

from MyPool import MyPool
from ..API.ArchiveAPI import ArchiveAPI

from TwitterCrawler import TwitterCrawler

from pprint import pprint

sys.setrecursionlimit(10000)


def parallelThread(poolSize, infoQueue, urlList, saveFolder, testCnt=None, timeout=1000, delay=None):

    #with open(file, "r", encoding='utf-8') as fin:
    #    urlList = eval(fin.read())

    pool = MyPool(poolSize, initThread, (infoQueue,))

    urlCnt = 0

    print("# of checking URLs is", len(urlList))

    for url in urlList:
        if url:
            pool.apply_async(timeoutThread, (url, saveFolder, timeout,))
            urlCnt += 1
            if delay:
                time.sleep(delay)

        if testCnt:
            if urlCnt == testCnt:
                break

    pool.close()
    pool.join()

    print("Finish main join")

    if infoQueue:
        infoQueue.put('Done')


def initThread(q):
    timeoutThread.q = q


# my timeout thread to avoid unreliable timeout in webdriver
def timeoutThread(url, saveFolder, timeout):
    startTime = time.time()
    infoQueue = None

    if hasattr(timeoutThread, 'q'):
        infoQueue = timeoutThread.q

    p = mp.Process(target=doTaskThread, args=(url, saveFolder, infoQueue,))
    p.daemon = True
    p.start()
    p.join(timeout)

    endTime = time.time()
    diffTime = endTime - startTime

    if p.is_alive():
        print('<ThreadTimeOut>cost %f for %s' % (diffTime, url))
        p.terminate()


def doTaskThread(url, saveFolder, infoQueue=None):
    crawler = TwitterCrawler()

    res = crawler.vt_more(url, saveFolder)

    if infoQueue and res:
        infoQueue.put(url)

def receiveThread(infoQueue, fnout):
    domains = []

    while True:
        message = infoQueue.get()
        #print(message)
        if message == 'Done':
            break

        domains.append(message)

    print("# ids queried: ", len(domains))
    with open(fnout, 'w', encoding='utf-8') as fout:
        pprint(domains, fout)

if __name__ == '__main__':

    processes = []
    infoQueue = mp.Queue()

    # testing
	with open("./accounturls/lfountain6655-2019-09-02", "r", encoding='utf-8') as f:
        acc_to_ids = eval(f.read())

    ids = set()
	for acc, id in acc_to_ids.items():
		ids.union(id)

    print("# ids: ", len(ids))

    #jobs = mp.cpu_count()
    jobs = 3
    processes.append(mp.Process(target=parallelThread, args=(jobs, infoQueue, domains, "./twitterids/")))
    processes.append(mp.Process(target=receiveThread, args=(infoQueue, "./idsqueried",)))

    for p in processes:
        p.start()

    # wait for process finished
    for p in processes:
        p.join()
