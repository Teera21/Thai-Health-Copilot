from langchain.memory import ConversationBufferMemory

class ExtendedConversationBufferMemory(ConversationBufferMemory):
    extra_variables:list[str] = []

    @property
    def memory_variables(self) -> list[str]:
        """Will always return list of memory variables."""
        return [self.memory_key] + self.extra_variables

    def load_memory_variables(self, inputs: dict[str, any]) -> dict[str, any]:
        """Return buffer with history and extra variables"""
        d = super().load_memory_variables(inputs)
        d.update({k:inputs.get(k) for k in self.extra_variables})        
        return d