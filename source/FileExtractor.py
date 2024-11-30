# Встроенные библиотеки
import io

# Сторонние библиотеки
from zipfile import ZipFile
from source.File import File,FileType

class FileExtractor:
    def extract(self, file: File) -> list:
        if file.type == FileType.Archive:
            return self.process_archive(file)
        else:
            return self.process_file(file)
        
    def process_archive(self, archive: File) -> list:
        extracted = []

        with ZipFile(io.BytesIO(archive.content), 'r') as _archive:
            for file in _archive.namelist():
                if file.endswith('.cs'):
                    with _archive.open(file) as binary:
                        file_contents = binary.read()
                        file_decoded = file_contents.decode("UTF-8")
                        extracted.append(file_decoded)
                        archive.neasted.append(File(FileType.File,file,file_decoded,None))
        return extracted

    def process_file(self, file: File) -> list:
        return [file.content.decode("UTF-8")]