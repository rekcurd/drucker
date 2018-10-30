#!/usr/bin/python
# -*- coding: utf-8 -*-

import drucker_pb2
import drucker_pb2_grpc

import json

from enum import Enum
from grpc._server import _Context
from typing import Iterator, Union

from logger.logger_interface import ServiceLoggerInterface
from core.predict_interface import PredictResult, PredictInterface

DruckerInput = Union[
    drucker_pb2.StringInput, drucker_pb2.BytesInput,
    drucker_pb2.ArrIntInput, drucker_pb2.ArrFloatInput, drucker_pb2.ArrStringInput]
DruckerOutput = Union[
    drucker_pb2.StringOutput, drucker_pb2.BytesOutput,
    drucker_pb2.ArrIntOutput, drucker_pb2.ArrFloatOutput, drucker_pb2.ArrStringOutput]


class DruckerWorkerServicer(drucker_pb2_grpc.DruckerWorkerServicer):
    class Type(Enum):
        STRING = 1
        BYTES = 2
        ARRAY_INT = 3
        ARRAY_FLOAT = 4
        ARRAY_STRING = 5

    def __init__(self, logger: ServiceLoggerInterface, predictor: PredictInterface):
        self.logger = logger
        self.predictor = predictor

    def Process(self,
                request: DruckerInput,
                response: DruckerOutput
                ) -> DruckerOutput:

        input = request.input
        try:
            ioption = json.loads(request.option.val)
        except:
            ioption = {request.option.val: request.option.val}

        single_output = self.predictor.get_type_output() in [self.Type.STRING, self.Type.BYTES]
        try:
            result = self.predictor.predict(input, ioption)
        except:
            if single_output:
                if isinstance(response, drucker_pb2.StringOutput):
                    label = "None"
                elif isinstance(response, drucker_pb2.BytesOutput):
                    label = b'None'
                else:
                    label = None
                result = PredictResult(label=label, score=0.0, option={})
            else:
                if isinstance(response, drucker_pb2.ArrStringOutput):
                    label = ["None"]
                elif isinstance(response, drucker_pb2.ArrIntOutput):
                    label = [0]
                elif isinstance(response, drucker_pb2.ArrFloatOutput):
                    label = [0.0]
                else:
                    label = None
                result = PredictResult(label=label, score=[0.0], option={})
        if single_output:
            response.output = result.label
            response.score = result.score
        else:
            response.output.extend(result.label)
            response.score.extend(result.score)
        response.option.val = result.option
        self.logger.emit(request, response, ioption.get('suppress_log_inout', False))
        return response

    def Predict_String_String(self,
                              request: drucker_pb2.StringInput,
                              context: _Context
                              ) -> drucker_pb2.StringOutput:
        response = drucker_pb2.StringOutput()
        self.predictor.set_type(self.Type.STRING, self.Type.STRING)
        return self.Process(request, response)

    def Predict_String_Bytes(self,
                             request: drucker_pb2.StringInput,
                             context: _Context
                             ) -> drucker_pb2.BytesOutput:
        response = drucker_pb2.BytesOutput()
        self.predictor.set_type(self.Type.STRING, self.Type.BYTES)
        yield self.Process(request, response)

    def Predict_String_ArrInt(self,
                              request: drucker_pb2.StringInput,
                              context: _Context
                              ) -> drucker_pb2.ArrIntOutput:
        response = drucker_pb2.ArrIntOutput()
        self.predictor.set_type(self.Type.STRING, self.Type.ARRAY_INT)
        return self.Process(request, response)

    def Predict_String_ArrFloat(self,
                                request: drucker_pb2.StringInput,
                                context: _Context
                                ) -> drucker_pb2.ArrFloatOutput:
        response = drucker_pb2.ArrFloatOutput()
        self.predictor.set_type(self.Type.STRING, self.Type.ARRAY_FLOAT)
        return self.Process(request, response)

    def Predict_String_ArrString(self,
                                 request: drucker_pb2.StringInput,
                                 context: _Context
                                 ) -> drucker_pb2.ArrStringOutput:
        response = drucker_pb2.ArrStringOutput()
        self.predictor.set_type(self.Type.STRING, self.Type.ARRAY_STRING)
        return self.Process(request, response)

    def Predict_Bytes_String(self,
                             request_iterator: Iterator[drucker_pb2.BytesInput],
                             context: _Context
                             ) -> drucker_pb2.StringOutput:
        for request in request_iterator:
            response = drucker_pb2.StringOutput()
            self.predictor.set_type(self.Type.BYTES, self.Type.STRING)
            return self.Process(request, response)

    def Predict_Bytes_Bytes(self,
                            request_iterator: Iterator[drucker_pb2.BytesInput],
                            context: _Context
                            ) -> drucker_pb2.BytesOutput:
        for request in request_iterator:
            response = drucker_pb2.BytesOutput()
            self.predictor.set_type(self.Type.BYTES, self.Type.BYTES)
            yield self.Process(request, response)

    def Predict_Bytes_ArrInt(self,
                             request_iterator: Iterator[drucker_pb2.BytesInput],
                             context: _Context
                             ) -> drucker_pb2.ArrIntOutput:
        for request in request_iterator:
            response = drucker_pb2.ArrIntOutput()
            self.predictor.set_type(self.Type.BYTES, self.Type.ARRAY_INT)
            return self.Process(request, response)

    def Predict_Bytes_ArrFloat(self,
                               request_iterator: Iterator[drucker_pb2.BytesInput],
                               context: _Context
                               ) -> drucker_pb2.ArrFloatOutput:
        for request in request_iterator:
            response = drucker_pb2.ArrFloatOutput()
            self.predictor.set_type(self.Type.BYTES, self.Type.ARRAY_FLOAT)
            return self.Process(request, response)

    def Predict_Bytes_ArrString(self,
                                request_iterator: Iterator[drucker_pb2.BytesInput],
                                context: _Context
                                ) -> drucker_pb2.ArrStringOutput:
        for request in request_iterator:
            response = drucker_pb2.ArrStringOutput()
            self.predictor.set_type(self.Type.BYTES, self.Type.ARRAY_STRING)
            return self.Process(request, response)

    def Predict_ArrInt_String(self,
                              request: drucker_pb2.ArrIntInput,
                              context: _Context
                              ) -> drucker_pb2.StringOutput:
        response = drucker_pb2.StringOutput()
        self.predictor.set_type(self.Type.ARRAY_INT, self.Type.STRING)
        return self.Process(request, response)

    def Predict_ArrInt_Bytes(self,
                             request: drucker_pb2.ArrIntInput,
                             context: _Context
                             ) -> drucker_pb2.BytesOutput:
        response = drucker_pb2.BytesOutput()
        self.predictor.set_type(self.Type.ARRAY_INT, self.Type.BYTES)
        yield self.Process(request, response)

    def Predict_ArrInt_ArrInt(self,
                              request: drucker_pb2.ArrIntInput,
                              context: _Context
                              ) -> drucker_pb2.ArrIntOutput:
        response = drucker_pb2.ArrIntOutput()
        self.predictor.set_type(self.Type.ARRAY_INT, self.Type.ARRAY_INT)
        return self.Process(request, response)

    def Predict_ArrInt_ArrFloat(self,
                                request: drucker_pb2.ArrIntInput,
                                context: _Context
                                ) -> drucker_pb2.ArrFloatOutput:
        response = drucker_pb2.ArrFloatOutput()
        self.predictor.set_type(self.Type.ARRAY_INT, self.Type.ARRAY_FLOAT)
        return self.Process(request, response)

    def Predict_ArrInt_ArrString(self,
                                 request: drucker_pb2.ArrIntInput,
                                 context: _Context
                                 ) -> drucker_pb2.ArrStringOutput:
        response = drucker_pb2.ArrStringOutput()
        self.predictor.set_type(self.Type.ARRAY_INT, self.Type.ARRAY_STRING)
        return self.Process(request, response)

    def Predict_ArrFloat_String(self,
                                request: drucker_pb2.ArrFloatInput,
                                context: _Context
                                ) -> drucker_pb2.StringOutput:
        response = drucker_pb2.StringOutput()
        self.predictor.set_type(self.Type.ARRAY_FLOAT, self.Type.STRING)
        return self.Process(request, response)

    def Predict_ArrFloat_Bytes(self,
                               request: drucker_pb2.ArrFloatInput,
                               context: _Context
                               ) -> drucker_pb2.BytesOutput:
        response = drucker_pb2.BytesOutput()
        self.predictor.set_type(self.Type.ARRAY_FLOAT, self.Type.BYTES)
        yield self.Process(request, response)

    def Predict_ArrFloat_ArrInt(self,
                                request: drucker_pb2.ArrFloatInput,
                                context: _Context
                                ) -> drucker_pb2.ArrIntOutput:
        response = drucker_pb2.ArrIntOutput()
        self.predictor.set_type(self.Type.ARRAY_FLOAT, self.Type.ARRAY_INT)
        return self.Process(request, response)

    def Predict_ArrFloat_ArrFloat(self,
                                  request: drucker_pb2.ArrFloatInput,
                                  context: _Context
                                  ) -> drucker_pb2.ArrFloatOutput:
        response = drucker_pb2.ArrFloatOutput()
        self.predictor.set_type(self.Type.ARRAY_FLOAT, self.Type.ARRAY_FLOAT)
        return self.Process(request, response)

    def Predict_ArrFloat_ArrString(self,
                                   request: drucker_pb2.ArrFloatInput,
                                   context: _Context
                                   ) -> drucker_pb2.ArrStringOutput:
        response = drucker_pb2.ArrStringOutput()
        self.predictor.set_type(self.Type.ARRAY_FLOAT, self.Type.ARRAY_STRING)
        return self.Process(request, response)

    def Predict_ArrString_String(self,
                                 request: drucker_pb2.ArrStringInput,
                                 context: _Context
                                 ) -> drucker_pb2.StringOutput:
        response = drucker_pb2.StringOutput()
        self.predictor.set_type(self.Type.ARRAY_STRING, self.Type.STRING)
        return self.Process(request, response)

    def Predict_ArrString_Bytes(self,
                                request: drucker_pb2.ArrStringInput,
                                context: _Context
                                ) -> drucker_pb2.BytesOutput:
        response = drucker_pb2.BytesOutput()
        self.predictor.set_type(self.Type.ARRAY_STRING, self.Type.BYTES)
        yield self.Process(request, response)

    def Predict_ArrString_ArrInt(self,
                                 request: drucker_pb2.ArrStringInput,
                                 context: _Context
                                 ) -> drucker_pb2.ArrIntOutput:
        response = drucker_pb2.ArrIntOutput()
        self.predictor.set_type(self.Type.ARRAY_STRING, self.Type.ARRAY_INT)
        return self.Process(request, response)

    def Predict_ArrString_ArrFloat(self,
                                   request: drucker_pb2.ArrStringInput,
                                   context: _Context
                                   ) -> drucker_pb2.ArrFloatOutput:
        response = drucker_pb2.ArrFloatOutput()
        self.predictor.set_type(self.Type.ARRAY_STRING, self.Type.ARRAY_FLOAT)
        return self.Process(request, response)

    def Predict_ArrString_ArrString(self,
                                    request: drucker_pb2.ArrStringInput,
                                    context: _Context
                                    ) -> drucker_pb2.ArrStringOutput:
        response = drucker_pb2.ArrStringOutput()
        self.predictor.set_type(self.Type.ARRAY_STRING, self.Type.ARRAY_STRING)
        return self.Process(request, response)