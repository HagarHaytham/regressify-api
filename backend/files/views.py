from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
import pandas as pd
from sklearn.linear_model import LinearRegression
import io
import matplotlib.pyplot as plt
from PIL import Image
import base64


class LinearRegressionView(APIView):

    parser_classes = (FileUploadParser,)

    def post(self, request, format=None):
        # if 'file' not in request.FILES:
        #     return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uploaded_file = request.FILES.get('file')  # Get the single uploaded file
            # print(uploaded_file)
            if uploaded_file:
                uploaded_file_name = uploaded_file.name
                uploaded_file_content = uploaded_file.read()

                n_lines = uploaded_file_content.decode('utf-8').split("\r\n\r\n", 1)[1]  # Split at the first double newline
                lines = n_lines.rstrip().splitlines()
                csv_data = "\n".join(lines[:-1])  # Join cleaned lines back into a string
                # print(csv_data)

                df = pd.read_csv(io.StringIO(csv_data))
                # print(df)
                X = df.iloc[:, :-1]  # All columns except the last

                y = df.iloc[:, -1]
                target_name = df.columns[-1]
                # print (y)
                # Perform linear regression
                model = LinearRegression()
                model.fit(X, y)

                # # Get regression coefficients and intercept
                # coefficients = model.coef_
                # intercept = model.intercept_

                # print(intercept)
                # # # Prepare response
                # response_data = {
                #     'coefficients': coefficients.tolist(),
                #     'intercept': intercept,
                #     'message': 'Linear regression completed successfully',
                # }
                # return Response(response_data, status=status.HTTP_200_OK)

                # Create the scatter plot
                plt.figure(figsize=(8, 6))
                plt.scatter(X, y, label='Actual')
                plt.plot(X, model.predict(X), color='red', label='Predicted')
                plt.xlabel(X.columns[0])
                plt.ylabel(target_name)
                plt.title('Scatter Plot with Linear Regression')
                plt.legend()

                # Convert plot to image
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_data = base64.b64encode(buf.read()).decode('utf-8')

                # Return image data in the response
                return Response({'image_data': image_data, 'message': 'Linear regression completed successfully',})


        except Exception as e:
            error_message = str(e)
            return Response({'status': 'error', 'message': error_message})

        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
