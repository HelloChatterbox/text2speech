from setuptools import setup

PLUGIN_ENTRY_POINT = ('chatterbox_gtts_plug = '
                      'text2speech.modules.google_tts:GoogleTTS',

                      'chatterbox_espeak_tts_plug = '
                      'text2speech.modules.espeak_tts:ESpeak',
                      'chatterbox_espeakng_tts_plug = '
                      'text2speech.modules.espeakng_tts:ESpeakNG',

                      'chatterbox_festival_tts_plug = '
                      'text2speech.modules.festival_tts:FestivalTTS',

                      'chatterbox_watson_tts_plug = '
                      'text2speech.modules.ibm_tts:WatsonTTS',

                      'chatterbox_mary_tts_plug = '
                      'text2speech.modules.mary_tts:MaryTTS',

                      'chatterbox_mbrola_tts_plug = '
                      'text2speech.modules.mbrola_tts:MbrolaTTS',

                      'chatterbox_mimic2_tts_plug = '
                      'text2speech.modules.mimic2_tts:Mimic2',
                      'chatterbox_mimic_tts_plug = '
                      'text2speech.modules.mimic_tts:Mimic',

                      'chatterbox_mozilla_tts_plug = '
                      'text2speech.modules.mozilla_tts:MozillaTTSServer',

                      'chatterbox_pico_tts_plug = '
                      'text2speech.modules.pico_tts:PicoTTS',

                      'chatterbox_polly_tts_plug = '
                      'text2speech.modules.polly_tts:PollyTTS',

                      'chatterbox_responsive_voice_tts_plug = '
                      'text2speech.modules.responsive_voice_tts:ResponsiveVoiceTTS',

                      'chatterbox_spdsay_tts_plug = '
                      'text2speech.modules.spdsay_tts:SpdSay',

                      'chatterbox_voicerss_tts_plug = '
                      'text2speech.modules.voice_rss:VoiceRSSTTS',

                      )

setup(
    name='text2speech',
    version='0.2.0a1',
    packages=['text2speech', 'text2speech.modules'],
    url='https://github.com/HelloChatterbox/text2speech',
    license='apache',
    author='jarbasAI',
    install_requires=["ovos_utils>=0.0.5",
                      "requests_futures",
                      "boto3",
                      "ResponsiveVoice",
                      "psutil",
                      "gTTS>=2.2.1",
                      "pyee==8.1.0",
                      "voxpopuli"],
    author_email='jarbasai@mailfence.com',
    description='TTS engines',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT}
)
