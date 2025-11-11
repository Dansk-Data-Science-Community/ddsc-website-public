class SaveEventMixin:
    def save_event(self):
        event = self.event_form.save(commit=False)
        event.draft = self.__get_draft_value()
        event.save()

        event_image = self.event_image_form.save(commit=False)
        address = self.address_form.save(commit=False)
        event_image.event = event
        event_image.order = 1
        address.event = event

        event_image.save()
        address.save()

    def __get_draft_value(self):
        return "save_draft" in self.request.POST
