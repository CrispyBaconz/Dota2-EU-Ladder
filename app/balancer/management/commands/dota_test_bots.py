from django.core.management.base import BaseCommand
import gevent
import dota2
import os
from steam import SteamClient
from dota2 import Dota2Client
from dota2.enums import DOTAChatChannelType_t, DOTA_GC_TEAM


class Command(BaseCommand):
    def __init__(self):
        self.bots = []
        self.lobby = None
        self.password = None

        self.balance_team1 = None

    def add_arguments(self, parser):
        parser.add_argument('-l', '--lobby', type=int)

        lobby_password = os.environ.get('LOBBY_PASSWORD', '')
        parser.add_argument('-p', '--password',
                            nargs='?', type=str,
                            default=lobby_password, const=lobby_password)

    def handle(self, *args, **options):
        self.lobby = options['lobby']
        self.password = options['password']

        bots_num = 9

        bot_login = os.environ.get('BOT_LOGIN', '')
        bot_password = os.environ.get('BOT_PASSWORD', '')
        credentials = [
            {
                'login': '%s%d' % (bot_login, i),
                'password': '%s%d' % (bot_password, i),
            } for i in xrange(2, bots_num+2)
        ]

        try:
            gevent.joinall([
                gevent.spawn(self.start_bot, c) for c in credentials
            ])
        finally:
            for bot in self.bots:
                bot.exit()
                bot.steam.logout()

    def start_bot(self, credentials):
        client = SteamClient()
        dota = Dota2Client(client)

        self.bots.append(dota)

        client.verbose_debug = True
        dota.verbose_debug = True

        @client.on('logged_on')
        def start_dota():
            dota.launch()

        @dota.on('ready')
        def dota_started():
            print 'Logged in: %s %s' % (dota.steam.username, dota.account_id)

            # if lobby is hung up from previous session, leave it
            dota.leave_practice_lobby()
            dota.join_practice_lobby(self.lobby, self.password)

        @dota.on(dota2.features.Lobby.EVENT_LOBBY_NEW)
        def lobby_new(lobby):
            print '%s joined lobby %s' % (dota.steam.username, lobby.lobby_id)

            ind = self.bots.index(dota)

            if ind == 0:
                # let first bot listen to lobby chat
                dota.join_lobby_chat()

            team = ind / 5
            slot = ind % 5 + 1
            dota.join_practice_lobby_team(slot, team)

        @dota.on(dota2.features.Lobby.EVENT_LOBBY_CHANGED)
        def lobby_changed(lobby):
            if dota != self.bots[0]:
                return

            players = [
                player for player in lobby.members
                if player.team in (DOTA_GC_TEAM.GOOD_GUYS, DOTA_GC_TEAM.BAD_GUYS)
            ]

            if len(players) == 0 and self.balance_team1:
                print
                print 'All bots jumped to unassigned'
                self.join_balance_slots()

        @dota.on(dota2.features.Chat.EVENT_CHAT_MESSAGE)
        def chat_message(channel, sender, text, msg_obj):
            if channel.channel_type != DOTAChatChannelType_t.DOTAChannelType_Lobby:
                return  # ignore postgame and other chats

            # process known commands
            if text.startswith('Team 1'):
                self.balance_ready(text)

        client.login(credentials['login'], credentials['password'])
        client.run_forever()

    def balance_ready(self, team1_text):
        print
        print 'Balance is ready'

        self.balance_team1 = team1_text.split(': ')[1].split(' | ')

        print 'Telling bots to free slots'
        for bot in self.bots:
            bot.join_practice_lobby_team()

    def join_balance_slots(self):
        print
        print 'Joining balanced slots'

        players_joined = [0, 0]
        for bot in self.bots:
            team = 0 if bot.steam.username in self.balance_team1 else 1
            players_joined[team] += 1
            bot.join_practice_lobby_team(players_joined[team], team)