import numpy as np
import os
from termcolor import colored
import time
import sys


# 添加新单词
def add_word(word, meaning, tag):
    """
    添加新的单词，或再次记录已经存在的单词。

    :param word: 单词
    :param meaning: 涵义
    :param tag: 词性
    :return: 无
    """
    if tag not in ['n', 'v', 'adj', 'adv', 'pron', 'prep', 'conj', 'interj', 'art', 'num', '']:
        raise ValueError(f"{tag} is not a reliable effective tag!")
    else:
        f = np.load("./data/words.npy", allow_pickle=True)
        wordlist = f[:, 0]
        if word not in wordlist:
            f = np.append(f, np.array([[word, meaning, tag, 1]]), axis=0)
        else:
            print(f"单词{word}曾经被记录了以下涵义：")
            exist_meaning_idx = np.where(f == word)[0]
            exist_meaning = f[exist_meaning_idx]
            # print(exist_meaning_idx)
            print(f"{word}:")
            for i in range(exist_meaning.shape[0]):
                print(f"[{i}] {exist_meaning[i][2]}. {exist_meaning[i][1]} 被记录过{exist_meaning[i][3]}次")
            num = input(f"已经包含了您想要添加的涵义吗？\n"
                        f"如果是的，为了使这个单词被记录到的次数加一，以便将来重点复习，请输入相同涵义对应的序号；\n"
                        f"如果想要添加一个新的涵义，请输入[new]；\n"
                        f"如果想要取消本次操作，请随便输入些无关的东西：")
            if num.isdigit():
                num = int(num)
                if num < exist_meaning.shape[0]:
                    f[exist_meaning_idx[num]][3] = str(int(f[exist_meaning_idx[num]][3]) + 1)
                    print(f"次数已更新："
                          f"[{num}] {f[exist_meaning_idx[num]][2]}. {f[exist_meaning_idx[num]][1]} "
                          f"被记录过{f[exist_meaning_idx[num]][3]}次")
                else:
                    print("输入了未知的命令，本次操作已取消")
            elif num == 'new':
                f = np.append(f, np.array([[word, meaning, tag, 1]]), axis=0)
            else:
                print("输入了未知的命令，本次操作已取消")

        np.save("./data/words", f)


# 查询单词
def search_word(word):
    """
    查找特定的单词。

    :param word: 单词
    :return: 无
    """
    f = np.load("./data/words.npy", allow_pickle=True)
    if word in f[:, 0]:
        # print(f"单词{word}曾经被记录了以下涵义：")
        exist_meaning_idx = np.where(f == word)[0]
        exist_meaning = f[exist_meaning_idx]
        # print(exist_meaning_idx)
        print(f"{word}:")
        for i in range(exist_meaning.shape[0]):
            num = int(exist_meaning[i][3])
            if num <= 2:
                print(f"[{i}] {exist_meaning[i][2]}. {exist_meaning[i][1]} 被记录过{exist_meaning[i][3]}次")
            elif num <= 5:
                print(colored(f"[{i}] {exist_meaning[i][2]}. {exist_meaning[i][1]} 被记录过{exist_meaning[i][3]}次", "blue"))
            elif num <= 8:
                print(colored(f"[{i}] {exist_meaning[i][2]}. {exist_meaning[i][1]} 被记录过{exist_meaning[i][3]}次", "magenta"))
            else:
                print(colored(f"[{i}] {exist_meaning[i][2]}. {exist_meaning[i][1]} 被记录过{exist_meaning[i][3]}次", "red"))
    else:
        print(f"单词{word}尚未被记录过。")


# 删除单词
def del_word(word):
    """
    删除某个单词。

    :param word: 单词
    :return: 无
    """
    f = np.load("./data/words.npy", allow_pickle=True)
    wordlist = f[:, 0]
    if word not in wordlist:
        print(f"单词表中不存在{word}！")
        time.sleep(1)
        os.system("cls")
    else:
        print(f"单词{word}曾经被记录了以下涵义：")
        exist_meaning_idx = np.where(f == word)[0]
        exist_meaning = f[exist_meaning_idx]
        # print(exist_meaning_idx)
        print(f"{word}:")
        for i in range(exist_meaning.shape[0]):
            print(f"[{i}] {exist_meaning[i][2]}. {exist_meaning[i][1]} 被记录过{exist_meaning[i][3]}次")
        num = input(f"包含了您想要删除的涵义吗？\n"
                    f"如果您想要删除某个释义，请输入对应的序号；\n"
                    f"如果如果您想要删除全部释义，请输入[all]；\n"
                    f"如果想要取消本次操作，请随便输入些无关的东西：")
        if num.isdigit():
            num = int(num)
            if num < exist_meaning.shape[0]:
                f = np.delete(f, exist_meaning_idx[num], axis=0)
                print(f"已删除")
                time.sleep(1)
                os.system("cls")
            else:
                print("输入了未知的命令，本次操作已取消")
        elif num == 'all':
            f = np.delete(f, exist_meaning_idx, axis=0)
            print(f"已删除")
            time.sleep(1)
            os.system("cls")
        else:
            print("输入了未知的命令，本次操作已取消")

        np.save("./data/words", f)


# 导出所有单词
def output_all(filename):
    """
    按照字母顺序导出所有单词。

    :param filename: 文件名
    :return: 无
    """
    f = np.load("./data/words.npy", allow_pickle=True)
    f = f[np.argsort(f[:, 0])]      # 按照字母顺序排序
    address = "./output/" + filename + ".txt"
    output_list = []

    this_time = time.localtime()
    with open(address, 'w') as fo:
        fo.write(f"{this_time.tm_year}-{this_time.tm_mon}-{this_time.tm_mday} 星期{this_time.tm_wday+1}\n")
        fo.write("按照字母顺序排列的单词表\n"
                 "===================\n")
        fo.write(f[0][0] + ":\n")
        fo.write(f"{('[' + str(0) + ']').ljust(4)} {(f[0][2] + '.').rjust(5)} {f[0][1].ljust(20, chr(12288))} "
                 f"{('被记录过' + f[0][3] + '次').ljust(8)}\n")
        order = 0
        for i in range(f.shape[0] - 1):
            if f[1:][i][0] == f[i][0]:
                order += 1
                fo.write(
                    f"{('[' + str(order) + ']').ljust(4)} {(f[1:][i][2] + '.').rjust(5)} {f[1:][i][1].ljust(20, chr(12288))} "
                    f"{('被记录过' + f[1:][i][3] + '次').ljust(8)}\n")
            else:
                order = 0
                fo.write("-------------------\n")
                fo.write(f[1:][i][0] + ":\n")
                fo.write(
                    f"{('[' + str(order) + ']').ljust(4)} {(f[1:][i][2] + '.').rjust(5)} {f[1:][i][1].ljust(20 , chr(12288))} "
                    f"{('被记录过' + f[1:][i][3] + '次').ljust(8)}\n")


def main():
    if not os.path.exists("./data"):
        print("第一次打开程序，创建数据文件夹...")
        os.mkdir("./data")
    if not os.path.exists("./data/words.npy"):
        print("单词数据不存在，创建单词数据...")
        np.save("./data/words", np.array([["apple", "苹果", "n", 1]]).astype(np.ndarray))
    else:
        while True:
            command = input("请输入命令（帮助：help）：\n")
            if command == "help":
                os.system("cls")
                print("可以使用的指令：\n"
                      "add 添加新单词\n"
                      "search 查询单词\n"
                      "delete 删除单词\n"
                      "output 输出所有单词到文本文件中\n"
                      f"{colored('close 关闭程序','red')}")
            elif command == "add":
                os.system("cls")
                word = input("要添加的单词：")
                meaning = input("涵义：")
                tag = input("词性：")
                add_word(word, meaning, tag)
                fake_load(1)
                os.system("cls")
            elif command == "search":
                os.system("cls")
                word = input("要查找的单词：")
                search_word(word)
                print("\n")
            elif command == "delete":
                os.system("cls")
                word = input("要删除的单词：")
                del_word(word)
                fake_load(2)
                time.sleep(1)
                os.system("cls")
            elif command == "output":
                os.system("cls")
                if not os.path.exists("./output"):
                    os.mkdir("./output")
                    os.system("cls")
                filename = input("文件名：")
                output_all(filename)
                fake_load(1)
                print("\n文本文件创建完成。")
                time.sleep(2)
                os.system("cls")
            elif command == "close":
                break
            else:
                print(f"未知的命令")
                time.sleep(1)
                os.system("cls")


def fake_load(sleep_time):
    for i in range(1, 101):
        print("\r", end="")
        print("进度: {}%: ".format(i), "▓" * (i // 2), end="")
        sys.stdout.flush()
        time.sleep(sleep_time/1000)

if __name__ == '__main__':
    os.system("cls")
    main()
