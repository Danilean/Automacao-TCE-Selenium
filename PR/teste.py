from fpdf import FPDF

# Criando a classe PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Documento de Relacao Familiar", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")

# Texto base para preencher as 30 linhas
texto = """
João Vitor Brogni Vamerlati é filho de Danilo Formanski, uma figura central em sua vida e em seu desenvolvimento como pessoa. Desde cedo, João Vitor teve a influência do pai em diversos aspectos, aprendendo com ele valores essenciais como respeito, responsabilidade e dedicação. A relação entre os dois sempre foi marcada por momentos de aprendizado e companheirismo, seja em atividades cotidianas ou em situações mais desafiadoras. Danilo sempre fez questão de estar presente, acompanhando as etapas e conquistas do filho, além de orientá-lo nas escolhas importantes.

Recentemente, Danilo tem sido uma grande inspiração para João Vitor também no mundo dos jogos, especialmente em League of Legends. Como um jogador mais experiente, Danilo constantemente dá um “gap” em João Vitor, dominando todos os campeões do jogo e aplicando estratégias que desafiam o filho a pensar mais rapidamente e aprender a lidar com diferentes habilidades e estilos de jogo. Essa competitividade saudável se torna um grande estímulo para João Vitor, que busca melhorar suas táticas e entendimento do jogo para conseguir acompanhar o ritmo do pai.

Danilo também mostra que perder faz parte do processo de evolução e que cada partida traz lições valiosas. Com essa base de desafios e incentivo, João Vitor está crescendo como player, ganhando resiliência e desenvolvendo habilidades como visão de mapa, controle de objetivos e esportividade. A cada partida, ele se torna um jogador mais completo e preparado para enfrentar adversários variados, e a parceria entre pai e filho, agora fortalecida dentro do mundo dos jogos, é um alicerce que impulsiona João Vitor a sempre buscar o próximo nível."""


texto = texto.replace("“", '"').replace("”", '"').replace("’", "'")


# Criando o PDF
pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, texto)

# Salvando o PDF
pdf_output_path = "./relacao_familiar.pdf"
pdf.output(pdf_output_path)

pdf_output_path
