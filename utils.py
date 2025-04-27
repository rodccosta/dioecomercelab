import base64

def gerar_data_uri(imagem_bytes, mime_type='image/jpeg'):
    # Codifica os bytes para base64
    imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')
    # Monta a data URI
    data_uri = f'data:{mime_type};base64,{imagem_base64}'
    return data_uri
