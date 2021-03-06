from page_objects import MultiPageElement, PageObject


class ListLinkDatePage(PageObject):
    li_dates = MultiPageElement(css=".date--item a")

    @property
    def dates(self):
        dates = map(lambda li_date: li_date.text, self.li_dates)
        return dates
