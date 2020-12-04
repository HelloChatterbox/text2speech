from setuptools import setup

setup(
    name='text2speech',
    version='0.1.7',
    packages=['text2speech', 'text2speech.modules'],
    url='https://github.com/HelloChatterbox/text2speech',
    license='apache',
    author='jarbasAI',
    install_requires=["ovos_utils",
                      "requests_futures",
                      "boto3",
                      "ResponsiveVoice",
                      "psutil",
                      "gTTS>=2.2.1",
                      "voxpopuli"],
    author_email='jarbasai@mailfence.com',
    description='TTS engines'
)
