#!/usr/bin/env python
#encoding: UTF-8

'''
网易云音乐 Ui
'''

import curses
from api import Api


class Ui:
    def __init__(self):
        self.screen = curses.initscr()
        # charactor break buffer
        curses.cbreak()
        self.screen.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)        

    def build_playinfo(self, song_name, artist, album_name):
    	self.screen.move(1,1)
    	self.screen.clrtoeol()
        self.screen.addstr(1, 9, '正在播放: ', curses.color_pair(3))
        self.screen.addstr(1, 19, song_name + '   -   ' + artist + '  < ' + album_name + ' >', curses.color_pair(2))
    	self.screen.refresh() 	

    def build_menu(self, datatype, title, datalist, offset, index, step):
    	# keep playing info in line 1
        self.screen.move(4,1)
        self.screen.clrtobot()
        self.screen.addstr(4, 19, title, curses.color_pair(1))

        if len(datalist) == 0:
            self.screen.addstr(8, 19, '未找到搜索结果 -，-')

        else:
            if datatype == 'main':
                for i in range( offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8, 16, '>> ' + str(i+1) + '. ' + datalist[i], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8, 19, str(i+1) + '. ' + datalist[i])

            elif datatype == 'songs':
                for i in range(offset, min( len(datalist), offset+step) ):
                    # this item is focus
                    if i == index:
                        self.screen.addstr(i - offset +8, 16, '>> ' + str(i+1) + '. ' + datalist[i]['song_name'] + '   -   ' + datalist[i]['artist'] + '  < ' + datalist[i]['album_name'] + ' >', curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8, 19, str(i+1) + '. ' + datalist[i]['song_name'] + '   -   ' + datalist[i]['artist'] + '  < ' + datalist[i]['album_name'] + ' >')
            
            elif datatype == 'artists':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8, 16, '>> ' + str(i+1) + '. ' + datalist[i]['artists_name'] + '   -   ' + str(datalist[i]['alias']), curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8, 19, str(i+1) + '. ' + datalist[i]['artists_name'] + '   -   ' + datalist[i]['alias'])

            elif datatype == 'albums':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8, 16, '>> ' + str(i+1) + '. ' + datalist[i]['albums_name'] + '   -   ' + datalist[i]['artists_name'], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8, 19, str(i+1) + '. ' + datalist[i]['albums_name'] + '   -   ' + datalist[i]['artists_name'])

            elif datatype == 'playlists':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8, 16, '>> ' + str(i+1) + '. ' + datalist[i]['playlists_name'] + '   -   ' + datalist[i]['creator_name'], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8, 19, str(i+1) + '. ' + datalist[i]['playlists_name'] + '   -   ' + datalist[i]['creator_name'])

        self.screen.refresh()    

    def build_search(self, stype):
    	api = Api()
        if stype == 'songs':
            song_name = self.get_param('搜索歌曲：')
            data = api.search(song_name, stype=1)
            song_ids = []
            if 'songs' in data['result']:
                if 'mp3Url' in data['result']['songs']:
                    songs = data['result']['songs']

                # search song result do not has mp3Url
                # send ids to get mp3Url
                else:
                    for i in range(0, len(data['result']['songs']) ):
                        song_ids.append( data['result']['songs'][i]['id'] )
                    data = api.songs_detail(song_ids)
                    songs = data['songs']
                return api.dig_info(songs, 'songs')
        
        elif stype == 'artists':
            artist_name = self.get_param('搜索艺术家：')
            data = api.search(artist_name, stype=100)
            if 'artists' in data['result']:
                artists = data['result']['artists']
                return api.dig_info(artists, 'artists')

        elif stype == 'albums':
            artist_name = self.get_param('搜索专辑：')
            data = api.search(artist_name, stype=10)
            if 'albums' in data['result']:
                albums = data['result']['albums']
                return api.dig_info(albums, 'albums')

        elif stype == 'playlists':
            artist_name = self.get_param('搜索网易精选集：')
            data = api.search(artist_name, stype=1000)
            if 'playlists' in data['result']:
                playlists = data['result']['playlists']
                return api.dig_info(playlists, 'playlists')


        return []

    def build_search_menu(self):
        self.screen.move(4,1)
        self.screen.clrtobot()
    	self.screen.addstr(7, 19, '选择搜索类型:', curses.color_pair(1))
    	self.screen.addstr(10,19, '[1] 歌曲')
    	self.screen.addstr(11,19, '[2] 艺术家')
    	self.screen.addstr(12,19, '[3] 专辑')
    	self.screen.addstr(13,19, '[4] 网易精选集')
    	self.screen.addstr(14,19, '[5] 用户')
    	self.screen.addstr(17,19, '请键入对应数字:', curses.color_pair(2))
    	self.screen.refresh()
    	x = self.screen.getch()
    	return x


    def get_param(self, prompt_string):
  		# keep playing info in line 1    	
        self.screen.move(4,1)
        self.screen.clrtobot()
        self.screen.addstr(5, 19, prompt_string, curses.color_pair(1))
        self.screen.refresh()
        input = self.screen.getstr(10, 19, 60)
        if input.strip() is '':
            return self.get_param(prompt_string)
        else:
            return input
