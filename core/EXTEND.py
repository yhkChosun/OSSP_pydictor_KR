#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2016-2022 LandGrey (https://github.com/LandGrey/pydictor)
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

from __future__ import unicode_literals

import os
import re
import itertools
from core.CONF import confcore
from lib.fun.decorator import magic
from lib.data.data import paths, pyoptions
from lib.fun.leetmode import leet_mode_magic
from lib.fun.fun import cool, walks_all_files, unique, charanger
from .korTOeng import *  # 한영 키보드 매핑
from .nameAPI import *  # 한영 이름변경 API import

try:
    import ConfigParser
except:
    import configparser as ConfigParser


def extend_magic(rawlist):
    if rawlist == []:
        exit(pyoptions.CRLF + cool.red("[-] raw extend resource cannot be empty"))
    leet = pyoptions.extend_leet

    @magic
    def extend():
        if pyoptions.more:
            for _ in walks_all_files(paths.weblist_path):
                yield "".join(_)
            for _ in walks_all_files(paths.syslist_path):
                yield "".join(_)
        for _ in extend_enter(rawlist, leet=leet):
            yield "".join(_)


def wordsharker(raw, leet=True):
    # raw word maybe strange case, both not lowercase and uppercase, such as 'myName'
    #
    init_word_res = []
    raw = str(raw).strip()  # raw에 args문자열 중 이름(한글) 저장됨.
    raw2 = translateName(raw)  # raw에 저장된 이름(한글)을 nameAPI를 이용해 다양한 경우의 영문이름으로 변환 후 raw2에 저장

    # 변환한 이름들을 성과 이름으로 분리, raw2_temp에 저장
    raw2_temp = []
    for i in range(len(raw2)):
        raw2_temp += raw2[i].split()

    raw3 = kor2eng(raw)  # raw에 저장된 이름(한글)을 영타로 변환 후 raw3에 저장 (ex- 김철수 --> rlacjftn )    # korTOeng.py에 존재하는 함수 이용
    temp_list = raw2_temp + raw3  # temp_list에 raw2_temp와 raw3의 결과 통합
    temp_set = set(temp_list)  # 리스트 내의 중복 데이터 제거 과정 1
    temp_list = list(temp_set)  # 리스트 내의 중복 데이터 제거 과정 2

    for raw in temp_list:  # 각각의 테이블 생성 알고리즘을 위에서 만든 temp_list 전체에 대해 수행하도록 수정함. (모든 한글이름 경우의 수에 대하여 수행)
        if not raw:
            return []
        # level {format}
        if pyoptions.level <= 5:
            # 5 {raw}
            init_word_res.append(raw)

        if pyoptions.level <= 4:
            # 4 {raw:lowercase}
            init_word_res.append(raw.lower())
            # 4 {Raw:capitalize}
            init_word_res.append(raw.capitalize())

        if pyoptions.level <= 3:
            # 3 {RAW:uppercase}
            init_word_res.append(raw.upper())

        if pyoptions.level <= 2:
            # 2 {raw}{raw}
            init_word_res.append(raw + raw)
            # 2 {raw:lowercase}{raw:lowercase}
            init_word_res.append(raw.lower() + raw.lower())
            # 2 {raw}{RAW:uppercase}
            init_word_res.append(raw + raw.upper())
            # 2 {raw:lowercase}{RAW:uppercase}
            init_word_res.append(raw.lower() + raw.upper())

        if pyoptions.level <= 1:
            # 1 {RAW:uppercase}{raw}
            init_word_res.append(raw.upper() + raw)
            # 1 {RAW:uppercase}{raw:lowercase}
            init_word_res.append(raw.upper() + raw.lower())
            # 1 {r:initials:lowercase}
            init_word_res.append(raw[0].lower())
            # 1 {R:initials:uppercase}
            init_word_res.append(raw[0].upper())
            # 1 {war:reverse}
            init_word_res.append(raw[::-1])
            # 1 {war:reverse:lowercase}
            init_word_res.append(raw[::-1].lower())
            # 1 {war:reverse:uppercase}
            init_word_res.append(raw[::-1].upper())

            # 1 {Raw:capitalize}{raw}
            init_word_res.append(raw.capitalize() + raw)
            # 1 {Raw:capitalize}{raw:lowercase}
            init_word_res.append(raw.capitalize() + raw.lower())
            # 1 {Raw:capitalize}{RAW:uppercase}
            init_word_res.append(raw.capitalize() + raw.upper())
            # 1 {Raw:capitalize}{Raw:capitalize}
            init_word_res.append(raw.capitalize() + raw.capitalize())
            # 1 {waR:capitalize:reverse}
            init_word_res.append(raw.capitalize()[::-1])
            # 1 {raW:reverse:capitalize:reverse}
            init_word_res.append(raw[::-1].capitalize()[::-1])
            # 1 {raw}{war:reverse}
            init_word_res.append(raw + raw[::-1])
            # 1 {raw}{war:reverse:lowercase}
            init_word_res.append(raw + raw[::-1].lower())
            # 1 {raw}{war:reverse:uppercase}
            init_word_res.append(raw + raw[::-1].upper())

        # 1337 mode
        if leet:
            for code in pyoptions.leetmode_code:
                init_word_res.append(leet_mode_magic(raw, code))

    return unique(init_word_res)


def extend_enter(rawlist, leet=True):
    extend_conf_dict = {'prefix': [], 'suffix': [], 'prefix_suffix': [], 'middle': []}
    try:
        config = ConfigParser.SafeConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(paths.extendconf_path)
        for s in config.sections():
            for o in config.options(s):
                extend_conf_dict[s].append(o)
    except Exception as e:
        exit(cool.red('[-] Parse extend cfg file error' + pyoptions.CRLF + cool.fuchsia('[!] ' + e.message)))

    res = []
    prefix_content = extend_conf_dict['prefix']
    suffix_content = extend_conf_dict['suffix']
    prefix_suffix_content = extend_conf_dict['prefix_suffix']
    middle_content = extend_conf_dict['middle']

    for raw in rawlist:
        shapers = wordsharker(raw, leet=leet)

        for middle in middle_content:
            matches = re.findall(pyoptions.level_str_pattern, middle)
            if matches:
                middles = []
                level = matches[0][0]
                middle = matches[0][1].strip()
                for key, value in pyoptions.charmap.items():
                    middle = middle.replace(key, value)

                if re.findall(pyoptions.rangepattern, middle):
                    middles.extend(charanger(middle[1:-1]))
                elif re.findall(pyoptions.confpattern, middle):
                    for m in confcore(middle):
                        middles.append(m)
                else:
                    middles.append(middle)
                middle_lenght = pyoptions.middle_switcher
                for m in middles:
                    if int(level) >= pyoptions.level:
                        for item in itertools.product(rawlist, repeat=2):
                            if len(item[0]) <= middle_lenght and len(item[1]) <= middle_lenght:
                                res.append(item[0] + m + item[1])
                        for item in itertools.product(shapers, repeat=2):
                            if len(item[0]) <= middle_lenght and len(item[1]) <= middle_lenght:
                                res.append(item[0] + m + item[1])

        shapers = wordsharker(raw, leet=leet)
        for w in shapers:
            res.append(w)
            for suffix in suffix_content:
                matches = re.findall(pyoptions.level_str_pattern, suffix)
                if matches:
                    tails = []
                    level = matches[0][0]
                    tail = matches[0][1].strip()
                    for key, value in pyoptions.charmap.items():
                        tail = tail.replace(key, value)
                    if re.findall(pyoptions.rangepattern, tail):
                        tails.extend(charanger(tail[1:-1]))
                    elif re.findall(pyoptions.confpattern, tail):
                        for t in confcore(tail):
                            tails.append(t)
                    else:
                        tails.append(tail)
                    for t in tails:
                        if int(level) >= pyoptions.level:
                            res.append(w + t)

            for prefix_suffix in prefix_suffix_content:
                matches = re.findall(pyoptions.level_str_str_pattern, prefix_suffix)
                if matches:
                    heads = []
                    tails = []
                    level = matches[0][0]
                    head = matches[0][1].strip()
                    tail = matches[0][2].strip()
                    for key, value in pyoptions.charmap.items():
                        head = head.replace(key, value)
                        tail = tail.replace(key, value)
                    if re.findall(pyoptions.rangepattern, head):
                        heads.extend(charanger(head[1:-1]))
                    elif re.findall(pyoptions.confpattern, head):
                        for h in confcore(head):
                            heads.append(h)
                    else:
                        heads.append(head)
                    if re.findall(pyoptions.rangepattern, tail):
                        tails.extend(charanger(tail[1:-1]))
                    elif re.findall(pyoptions.confpattern, tail):
                        for t in confcore(tail):
                            tails.append(t)
                    else:
                        tails.append(tail)
                    for h in heads:
                        for t in tails:
                            if int(level) >= pyoptions.level:
                                res.append(h + w + t)

            for prefix in prefix_content:
                matches = re.findall(pyoptions.level_str_pattern, prefix)
                if matches:
                    heads = []
                    level = matches[0][0]
                    head = matches[0][1].strip()
                    for key, value in pyoptions.charmap.items():
                        head = head.replace(key, value)
                    if re.findall(pyoptions.rangepattern, head):
                        heads.extend(charanger(head[1:-1]))
                    elif re.findall(pyoptions.confpattern, head):
                        for h in confcore(head):
                            heads.append(h)
                    else:
                        heads.append(head)
                    for h in heads:
                        if int(level) >= pyoptions.level:
                            res.append(h + w)

    return unique(res)


def get_extend_dic(target):
    rawlist = []
    for t in target:
        if os.path.isfile(t):
            with open(t) as f:
                for line in f:
                    rawlist.append(line.strip())
        else:
            rawlist.append(t)
    extend_magic(rawlist)

