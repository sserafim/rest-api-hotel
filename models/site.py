from sql_alchemy import banco


# Cria um objeto model da clase HotelModel
class SiteModel(banco.Model):

    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    # Cria os campos do modelo da classe hotel >>Isso é um objeto<<
    def __init__(self, url):
        self.url = url

    # Funcão que Transforma um objeto em um fomato DICIONÁRIO que converte/ou é um JSON - automaticamente >>>  <<<

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        url = cls.query.filter_by(url=url).first()
        if url:
            return url
        return None

    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, url):
        self.url = url

    def delete_site(self):
        # Deletando todos os hoteis associado ao site
        [hotel.delete_hotel() for hotel in self.hoteis]
        # Agora deleta o site
        banco.session.delete(self)
        banco.session.commit()
