from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git
import os
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def update(request):
    if request.method == "POST":
        repo_path = '/home/Brunops52/book_store'
        
        try:
            # Verificação adicional
            if not os.path.exists(repo_path):
                logger.error(f"Diretório não encontrado: {repo_path}")
                return HttpResponse("Diretório do projeto não encontrado", status=500)
            
            if not os.path.exists(os.path.join(repo_path, '.git')):
                logger.error(f"Diretório .git não encontrado em: {repo_path}")
                return HttpResponse("Repositório Git não encontrado", status=500)
            
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            
            # Log antes do pull
            logger.info(f"Antes do pull - HEAD: {repo.head.commit}")
            
            origin.pull()
            
            # Log após o pull
            logger.info(f"Após o pull - HEAD: {repo.head.commit}")
            
            return HttpResponse("Código atualizado com sucesso!", status=200)
            
        except Exception as e:
            logger.error(f"Erro durante atualização: {str(e)}", exc_info=True)
            return HttpResponse(f"Erro durante atualização: {str(e)}", status=500)
    
    return HttpResponse("Método não permitido", status=405)
