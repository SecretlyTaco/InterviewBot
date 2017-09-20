# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3

WELCOME_MESSAGE = "Hi %s! Please read the interview questions at this link, type \"!queue\" without the quotes when you're ready to start the interview: https://<pastebin link with questions> "

@irc3.plugin
class Plugin:

    def __init__(self, bot):
        self.bot = bot
        self.qq = []

    @irc3.event(irc3.rfc.JOIN)
    def say_hi(self, mask, channel, **kw):
        """Say hi when someone join a channel"""
        if mask.nick != self.bot.nick:
            self.bot.privmsg(channel, WELCOME_MESSAGE % mask.nick)
        else:
            self.bot.privmsg(channel, 'Hi!')

    @command(permission='view')
    def queue(self, mask, target, args):
        """Join the queue

            %%queue
        """
        if mask.nick in self.qq:
            self.bot.privmsg(channel, 'Already #%s in queue' % str(1+int(self.qq.index(mask.nick))))
        else:
            self.qq.append(mask.nick)
            print(self.qq) #Print queue in terminal
            self.bot.privmsg(channel, "Added to queue. You are #%s" % str(len(self.qq)))

    @irc3.event(irc3.rfc.PART)
    def rm_from_queue(self, mask, channel, **kw):
        """Remove someone from the queue if they leave the channel"""
        try:
            self.qq.remove(mask.nick)
        except: #Bad code, I know
            pass

    @command(permission='mod')
    def next(self, mask, channel, target):
        """Get next person from queue
        
           %%next
        """
        if len(self.qq) > 0:
            np = self.qq[0]
            del self.qq[0]
            self.bot.privmsg(channel, 'Next person in queue is %s' % np)
        else:
            self.bot.privmsg(channel, 'Queue is empty')

    @command(permission='mod')
    def bbq(self, mask, channel, args):
        """Remove someone from queue
        
           %%bbq <name>
        """
        try:
            self.qq.remove(args['<name>'])
            self.bot.privmsg(channel, 'Removed %s from queue' % args['<name>'])
        except ValueError:
            self.bot.privmsg(channel, 'Couldn\'t find %s in queue' % args['<name>'])

    @command(permission='admin', show_in_help_list=False, public=False)
    def sendraw(self, mask, target, args):
        """Send raw message to IRC as bot
        
           %%sendraw <command>...
        """
        self.bot.send_line(' '.join(args['<command>']))
