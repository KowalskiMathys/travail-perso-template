class DocumentInfos:

    title = u'Résoudre des sudoku avec les métaheuristiques'
    first_name = 'Mathys'
    last_name = 'Kowalski'
    author = f'{first_name} {last_name}'
    year = u'2023'
    month = u'Mai'
    seminary_title = u'Travail personnel OCI'
    tutor = u"Cédric Donner"
    release = "(Version Finale)"
    repository_url = "https://github.com/<username>/<reponame>"

    @classmethod
    def date(cls):
        return cls.month + " " + cls.year

infos = DocumentInfos()