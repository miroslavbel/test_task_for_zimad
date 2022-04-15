from typing import Optional

from dataclasses import dataclass
from datetime import date

import fitz
from fitz.fitz import Document, Page


@dataclass
class PdfInfo:
    """
    У всех полей, которые не были заполнены в примере поставил тип `Optional[str]`
    """

    name: str
    pn: str
    description: Optional[str]
    location: Optional[str]
    receiver: int
    exp_date: Optional[str]
    cert_source: Optional[str]
    rec_date: date
    batch: Optional[str]
    remark: str
    tagged_by: Optional[str]
    sn: Optional[str]
    condition: str
    uom: str
    po: str
    mfg: Optional[str]
    dom: Optional[str]
    lot: Optional[str]
    notes: Optional[str]
    quantity: int


class PdfFile:
    def __init__(self, path: str):
        """
        Сразу не открываем, так как `fitz` сам открывает файл.

        :param path: путь к файлу
        """
        self._path = path

    def get_pdf_info(self) -> PdfInfo:
        """
        Собирает в словарь информацию из документа.

        Не обрабатывает ошибки возникающие если на вход подан документ другого формата.

        :return: прочитанная из документа информация
        """
        doc: Document = fitz.open(self._path)
        assert doc.page_count == 1, "Document should contain only one page"
        page: Page = doc.load_page(0)
        dict_data: dict = page.get_text("dict")
        blocks = dict_data.get("blocks")
        assert blocks is not None and len(blocks) == 12, "Unsupported format"

        name = blocks[0]["lines"][0]["spans"][0]["text"]
        pn = blocks[1]["lines"][0]["spans"][1]["text"]
        sn = (
            blocks[1]["lines"][1]["spans"][1]["text"]
            if len(blocks[1]["lines"][1]["spans"]) == 2
            else None
        )
        description = (
            blocks[2]["lines"][0]["spans"][1]["text"]
            if len(blocks[2]["lines"][0]["spans"]) == 2
            else None
        )
        location = (
            blocks[2]["lines"][1]["spans"][1]["text"]
            if len(blocks[2]["lines"][1]["spans"][0]["text"]) == 2
            else None
        )
        condition = blocks[2]["lines"][2]["spans"][1]["text"]
        receiver = blocks[3]["lines"][0]["spans"][1]["text"]
        uom = blocks[3]["lines"][1]["spans"][1]["text"]
        exp_date = (
            blocks[4]["lines"][0]["spans"][1]["text"]
            if len(blocks[4]["lines"][0]["spans"]) == 2
            else None
        )
        po = blocks[4]["lines"][1]["spans"][1]["text"]
        cert_source = (
            blocks[5]["lines"][0]["spans"][1]["text"]
            if len(blocks[5]["lines"][0]["spans"]) == 2
            else None
        )
        rec_date = date.fromisoformat(blocks[5]["lines"][1]["spans"][1]["text"])
        mfg = (
            blocks[5]["lines"][2]["spans"][1]["text"]
            if len(blocks[5]["lines"][2]["spans"]) == 2
            else None
        )
        batch = (
            blocks[6]["lines"][0]["spans"][1]["text"]
            if len(blocks[6]["lines"][0]["spans"]) == 2
            else None
        )
        dom = (
            blocks[6]["lines"][1]["spans"][1]["text"]
            if len(blocks[6]["lines"][1]["spans"]) == 2
            else None
        )
        remark = (
            blocks[7]["lines"][0]["spans"][1]["text"]
            if len(blocks[7]["lines"][0]["spans"]) == 2
            else None
        )
        lot = (
            blocks[7]["lines"][1]["spans"][1]["text"]
            if len(blocks[7]["lines"][1]["spans"]) == 2
            else None
        )
        tagged_by = (
            blocks[8]["lines"][0]["spans"][1]["text"]
            if len(blocks[8]["lines"][0]["spans"]) == 2
            else None
        )
        quantity = int(blocks[10]["lines"][0]["spans"][0]["text"][5:])
        notes = (
            blocks[11]["lines"][0]["spans"][1]["text"]
            if len(blocks[11]["lines"][0]["spans"]) == 2
            else None
        )

        return PdfInfo(
            name=name,
            pn=pn,
            description=description,
            location=location,
            receiver=receiver,
            exp_date=exp_date,
            cert_source=cert_source,
            rec_date=rec_date,
            batch=batch,
            remark=remark,
            tagged_by=tagged_by,
            sn=sn,
            condition=condition,
            uom=uom,
            po=po,
            mfg=mfg,
            dom=dom,
            lot=lot,
            notes=notes,
            quantity=quantity,
        )


if __name__ == "__main__":
    pass
