# Atena
 
Atena é o sistema modular responsável por várias atividades de gestão na SEE/AC.
O sistema é dividido em módulos sendo cada um responsável por uma aplicação que, na
maioria das vezes, podem comunicar entre si. 

 
# Tecnologias 
 
Aqui estão as tecnologias utilizadas neste projeto.
 
* Django: 3.2.9
* Mysql: 8.0.28
* Nginx:Latest
 
 
## Serviços usados
 
* Docker
* Git Flow 

## Nota importante antes de realizar o deploy da aplicação
 **Tenha instalado na sua máquna o Docker.**
 
# Passos para subir o projeto
 
Criar um clone do repositório:
```bash
  $ git clone https://github.com/seesistemas/Atena.git
```

Entre na pasta do repositório:
```bash
  $ cd Atena/
```

Execute  comando docker para subir nossas aplicações:
```bash
  $ docker-compose up --build -d
```