#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import time
import re

class Source (object) :

    def __init__ (self):
        self.T = tools.Tools()
        self.now = int(time.time() * 1000)

    def getSource (self) :
        urlList = []
        url = 'https://raw.githubusercontent.com/joevess/IPTV/refs/heads/main/m3u/iptv.m3u'
        # url = 'https://raw.githubusercontent.com/billy21/Tvlist-awesome-m3u-m3u8/master/m3u/%E5%9B%BD%E5%86%85.m3u'
        # url = 'https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/m3u/itv.m3u'
        # url = 'https://raw.githubusercontent.com/jisoypub/iptv/refs/heads/master/cn_all.m3u'
        req = [
            'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
        ]
        res = self.T.getPage(url, req)

        if res['code'] == 200 :
            pattern = re.compile(r"#EXTM3U(.*?)\n(.*)", re.I | re.S)
            tmp = pattern.findall(res['body'])
            pattern = re.compile(
                r"#EXTINF:-1 (.*?)\n(.*?)\n#EXTINF:-1", re.I | re.S)
            sourceList = pattern.findall(tmp[0][1])
            i = 1
            total = len(sourceList)
            for item in sourceList :
                info = self.T.fmtTitle(item[0])
                self.T.logger('正在分析[ %s / %s ]: %s' % (i, total, str(info['id']) + str(info['title'])))

                netstat = self.T.chkPlayable(item[1])
                i = i + 1
                if netstat > 0 :
                    cros = 1 if self.T.chkCros(item[1]) else 0
                    data = {
                        'title'  : str(info['id']) if info['id'] != '' else str(info['title']),
                        'url'    : str(item[1]),
                        'quality': str(info['quality']),
                        'delay'  : netstat,
                        'cros'   : cros,
                        'level'  : info['level'],
                        'online' : 1,
                        'udTime' : self.now,
                    }
                    urlList.append(data)
                else :
                    pass # MAYBE later :P
        else :
            pass # MAYBE later :P

        return urlList
