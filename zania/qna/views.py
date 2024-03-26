import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from zania.qna.utils import parse_pdf_file
from zania.qna.openai import get_open_ai_answer

class QnaBotAPIView(APIView):
    parser_classes = (MultiPartParser,)
    
    def post(self, request):
        try:
            if 'questions' not in request.FILES:
                return Response({"error": "questions file is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            if 'content' not in request.FILES:
                return Response({"error": "content file is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            questions = request.FILES['questions']
            content = request.FILES['content']
            
            if questions.name.split('.')[1] != 'json' or content.name.split('.')[1] != 'pdf':
                return Response({"error": "Unsupported file type"}, status=status.HTTP_400_BAD_REQUEST)
            
            parsed_questions_file = json.load(questions)
            parsed_content_file = parse_pdf_file(content)
            
            answers = get_open_ai_answer(documents=parsed_content_file, questions=parsed_questions_file)
            
            return Response(answers, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception in QnaBotAPIView: ", e)
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)