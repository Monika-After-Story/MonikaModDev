# Copyright (c) 1999-2016 Carnegie Mellon University. All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# This work was supported in part by funding from the Defense Advanced
# Research Projects Agency and the National Science Foundation of the
# United States of America, and the CMU Sphinx Speech Consortium.
#
# THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
# NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import os
import sys
import signal
from contextlib import contextmanager
from sphinxbase import *
from .pocketsphinx import *


DefaultConfig = Decoder.default_config


def get_model_path():
    """ Return path to the model. """
    return os.path.join(os.path.dirname(__file__), 'model')


def get_data_path():
    """ Return path to the data. """
    return os.path.join(os.path.dirname(__file__), 'data')


class Pocketsphinx(Decoder):

    def __init__(self, **kwargs):
        model_path = get_model_path()
        data_path = get_data_path()

        self.goforward = os.path.join(data_path, 'goforward.raw')

        if kwargs.get('dic') is not None and kwargs.get('dict') is None:
            kwargs['dict'] = kwargs.pop('dic')

        if kwargs.get('hmm') is None:
            kwargs['hmm'] = os.path.join(model_path, 'en-us')

        if kwargs.get('lm') is None:
            kwargs['lm'] = os.path.join(model_path, 'en-us.lm.bin')

        if kwargs.get('dict') is None:
            kwargs['dict'] = os.path.join(model_path, 'cmudict-en-us.dict')

        if kwargs.pop('verbose', False) is False:
            if sys.platform.startswith('win'):
                kwargs['logfn'] = 'nul'
            else:
                kwargs['logfn'] = '/dev/null'

        config = DefaultConfig()

        for key, value in kwargs.items():
            if isinstance(value, bool):
                config.set_boolean('-{}'.format(key), value)
            elif isinstance(value, int):
                config.set_int('-{}'.format(key), value)
            elif isinstance(value, float):
                config.set_float('-{}'.format(key), value)
            elif isinstance(value, str):
                config.set_string('-{}'.format(key), value)

        super(Pocketsphinx, self).__init__(config)

    def __str__(self):
        return self.hypothesis()

    @contextmanager
    def start_utterance(self):
        self.start_utt()
        yield
        self.end_utt()

    @contextmanager
    def end_utterance(self):
        self.end_utt()
        yield
        self.start_utt()

    def decode(self, audio_file=None, buffer_size=2048,
               no_search=False, full_utt=False):
        buf = bytearray(buffer_size)
        with open(audio_file or self.goforward, 'rb') as f:
            with self.start_utterance():
                while f.readinto(buf):
                    self.process_raw(buf, no_search, full_utt)
        return self

    def segments(self, detailed=False):
        if detailed:
            return [
                (s.word, s.prob, s.start_frame, s.end_frame)
                for s in self.seg()
            ]
        else:
            return [s.word for s in self.seg()]

    def hypothesis(self):
        hyp = self.hyp()
        if hyp:
            return hyp.hypstr
        else:
            return ''

    def probability(self):
        hyp = self.hyp()
        if hyp:
            return hyp.prob

    def score(self):
        hyp = self.hyp()
        if hyp:
            return hyp.best_score

    def best(self, count=10):
        return [
            (h.hypstr, h.score)
            for h, i in zip(self.nbest(), range(count))
        ]

    def confidence(self):
        hyp = self.hyp()
        if hyp:
            return self.get_logmath().exp(hyp.prob)


class AudioFile(Pocketsphinx):

    def __init__(self, **kwargs):
        signal.signal(signal.SIGINT, self.stop)

        self.audio_file = kwargs.pop('audio_file', None)
        self.buffer_size = kwargs.pop('buffer_size', 2048)
        self.no_search = kwargs.pop('no_search', False)
        self.full_utt = kwargs.pop('full_utt', False)

        self.keyphrase = kwargs.get('keyphrase')

        self.in_speech = False
        self.buf = bytearray(self.buffer_size)

        super(AudioFile, self).__init__(**kwargs)

        self.f = open(self.audio_file or self.goforward, 'rb')

    def __iter__(self):
        with self.f:
            with self.start_utterance():
                while self.f.readinto(self.buf):
                    self.process_raw(self.buf, self.no_search, self.full_utt)
                    if self.keyphrase and self.hyp():
                        with self.end_utterance():
                            yield self
                    elif self.in_speech != self.get_in_speech():
                        self.in_speech = self.get_in_speech()
                        if not self.in_speech and self.hyp():
                            with self.end_utterance():
                                yield self

    def stop(self, *args, **kwargs):
        raise StopIteration


class LiveSpeech(Pocketsphinx):

    def __init__(self, **kwargs):
        signal.signal(signal.SIGINT, self.stop)

        self.audio_device = kwargs.pop('audio_device', None)
        self.sampling_rate = kwargs.pop('sampling_rate', 16000)
        self.buffer_size = kwargs.pop('buffer_size', 2048)
        self.no_search = kwargs.pop('no_search', False)
        self.full_utt = kwargs.pop('full_utt', False)

        self.keyphrase = kwargs.get('keyphrase')

        self.in_speech = False
        self.buf = bytearray(self.buffer_size)
        self.ad = Ad(self.audio_device, self.sampling_rate)

        super(LiveSpeech, self).__init__(**kwargs)

    def __iter__(self):
        with self.ad:
            with self.start_utterance():
                while self.ad.readinto(self.buf) >= 0:
                    self.process_raw(self.buf, self.no_search, self.full_utt)
                    if self.keyphrase and self.hyp():
                        with self.end_utterance():
                            yield self
                    elif self.in_speech != self.get_in_speech():
                        self.in_speech = self.get_in_speech()
                        if not self.in_speech and self.hyp():
                            with self.end_utterance():
                                yield self

    def stop(self, *args, **kwargs):
        raise StopIteration
