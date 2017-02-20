from flask_ask import statement, audio, question, session
from alexa import ask
from alexa.utils.youtube import Youtube
from alexa.utils.config import LocalConfig
from flask import request
import logging

config = LocalConfig()
youtube = Youtube(session=session)


@ask.intent("PersonalPiePlayYoutube")
def play_youtube(search_query):
    youtube.search(search_query)

    current = youtube.current()

    youtube.save_session()
    return audio("Playing %s" % current.title).play(current.stream_url)


@ask.intent("PersonalPiePlayYoutubeNext")
def play_next_intent():
    logging.debug('From alexa: received next intent')

    current = youtube.next()
    if current is not None:
        youtube.save_session()
        return audio().play(current.stream_url)

    return audio("There are no more songs in the queue")


@ask.on_playback_stopped()
def stopped(offset):
    logging.debug('From alexa: stopped at: %s' % str(offset))


@ask.on_playback_started()
def started(offset):
    logging.debug('From alexa: started at: %s' % str(offset))


@ask.on_playback_nearly_finished()
def nearly_finished():
    logging.debug('From alexa: nearly finished')

    current = youtube.next()
    if current is not None:
        youtube.save_session()
        return audio().enqueue(current.stream_url)


@ask.on_playback_finished()
def playback_finished():
    logging.debug('From alexa: playback finished')


@ask.launch
def login():
    text = 'Welcome to %s.' % config.general['name']
    prompt = ''' Here are some things you can say:
        Play something
        How is the weather
    '''
    return question(text).reprompt(prompt)


@ask.intent('AudioPlayer.PlaybackFailed')
def error_playback():
    logging.debug('From alexa: error playback: %s' % str(request.args))
    return statement("I cannot play the selected sound")


@ask.intent("AMAZON.HelpIntent")
def help_me():
    text = ''' Here are some things you can say:
        Play something
        How is the weather
    '''

    prompt = 'For example say, Play disturbed'
    return question(text).reprompt(prompt)


@ask.intent('AMAZON.ResumeIntent')
def playback_resume():
    return audio('Resuming').resume()


@ask.intent('AMAZON.PauseIntent')
def playback_pause():
    return audio('Pausing').stop()


@ask.intent('AMAZON.StopIntent')
def playback_stop():
    youtube.clear()
    return audio('Stopping').stop()


@ask.intent('AMAZON.NextIntent')
def playback_next():
    logging.debug('From alexa: received next intent')

    current = youtube.next()
    if current is not None:
        youtube.save_session()
        return audio().play(current.stream_url)

    return audio("There are no more songs in the queue")


@ask.intent('AMAZON.PreviousIntent')
def playback_prev():
    logging.debug('From alexa: received prev intent')

    current = youtube.prev()
    if current is not None:
        youtube.save_session()
        return audio().play(current.stream_url)

    return audio("There are no more songs in the queue")
