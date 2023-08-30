from typing import Any, List, Union, Tuple
from steamship.agents.schema import AgentContext, Tool
from steamship import Block
from goplus.token import Token
from goplus.address import Address
from goplus.nft import Nft
from goplus.approve import Approve
from steamship.utils.repl import ToolREPL
from goplus.dapp import Dapp
from goplus.decode import Decode
from goplus.phishing_site import PushingSite

# Define a dictionary to map command names to their corresponding methods
COMMANDS = {
    "check_token_security": "check_token_security",
    "check_malicious_address": "check_malicious_address",
    "check_nft_security": "check_nft_security",
    "check_approval_security": "check_approval_security",
    "check_phishing_site": "check_phishing_site",
    "check_abi_decode": "check_abi_decode",
    "check_dapp_security": "check_dapp_security"
}

class GoPlusSecurityTool(Tool):
    """
    Custom Steamship tool for performing various Security checks on web3 using GoPlus API.
    """
    name: str = "GoPlusSecurityTool"
    human_description: str = "Perform various Security checks on web3 using GoPlus API"
    agent_description: str = """
    Used to perform real-time, dynamic, and automated security checks on web3 infrastructure including Token Security, NFT Security, Malicious Address, Approval Security, dApp Security Info, and Signature Data Decode APIs.
    """
  
    def run(self, tool_input: List[Block], context: AgentContext) -> Union[List[Block], Any]:
        """
        Execute the Security check using the GoPlus API.
        """
        print(context.chat_history)
        output = []
        for block in tool_input:
            if block.is_text():
                if not self.matches(block.text):
                    return "Invalid command"
                args = self.get_command_for(block.text)
                cmd = args[0]
                if cmd in COMMANDS:
                    method = getattr(self, COMMANDS[cmd])
                    data = method(args[1])
                    output.append(Block(text=str(data)))
                else:
                    return "Invalid command"
        return output

    def get_command_for(self, text: str) -> Tuple[str, List[str]]:
        """
        Extracts the command and its arguments from the given text.
        """
        words = text.split()
        for i, word in enumerate(words):
            if word in COMMANDS:
                command = word
                args = words[i+1:]
                return command, args
        return None, []

    def matches(self, s: str) -> bool:
        """
        Checks if the incoming chat message contains a known command.
        """
        cmd, args = self.get_command_for(s)
        return cmd is not None

    # Below are the methods for each specific security check, which call the corresponding GoPlus API methods.

    def check_token_security(self, token_args: List[str]) -> str:
        data = Token(access_token=None).token_security(chain_id=token_args[1], addresses=[token_args[0]])
        return data

    def check_malicious_address(self, address_arg: List[str]) -> str:
        data = Address(access_token=None).address_security(address_arg[0])
        return data

    def check_nft_security(self, nft_arg: List[str]) -> str:
        data = Nft(access_token=None).nft_security(address=nft_arg[0], chain_id=nft_arg[1])
        return data

    def check_approval_security(self, approval_arg: List[str]) -> str:
        data = Approve(access_token=None).token_approve_security(address=approval_arg[0], chain_id=approval_arg[1])
        return data

    def check_dapp_security(self, dapp_arg: List[str]) -> str:
        data = Dapp(access_token=None).dapp_security(dapp_arg[0])
        return data

    def check_abi_decode(self, abi_arg: List[str]) -> str:
        data = Decode(access_token=None).signature_data_decode(
            address=abi_arg[0], chain_id=abi_arg[1], data=abi_arg[2]
        )
        return data

    def check_phishing_site(self, site_arg: List[str]) -> str:
        data = PushingSite(access_token=None).pushing_site_security(site_arg[0])
        return data

# Note: You would typically integrate this custom tool into your Steamship workspace.
# The example above is a standalone representation.
if __name__ == "__main__":
    tool = GoPlusSecurityTool()
    ToolREPL(tool).run()
