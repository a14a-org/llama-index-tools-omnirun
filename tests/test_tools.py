"""Unit tests for llama-index-tools-omnirun (mocked, no API keys needed)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestOmniRunToolSpec:
    def test_default_template(self):
        from llama_index_tools_omnirun import OmniRunToolSpec

        spec = OmniRunToolSpec()
        assert spec.template == "python-3.11"
        assert spec.timeout == 30

    def test_custom_template(self):
        from llama_index_tools_omnirun import OmniRunToolSpec

        spec = OmniRunToolSpec(template="node-20", timeout=60)
        assert spec.template == "node-20"
        assert spec.timeout == 60

    def test_to_tool_list_returns_four(self):
        from llama_index_tools_omnirun import OmniRunToolSpec

        spec = OmniRunToolSpec()
        tools = spec.to_tool_list()
        assert len(tools) == 4
        names = {t.metadata.name for t in tools}
        assert names == {
            "omnirun_execute",
            "omnirun_shell",
            "omnirun_write_file",
            "omnirun_read_file",
        }

    def test_tool_descriptions(self):
        from llama_index_tools_omnirun import OmniRunToolSpec

        spec = OmniRunToolSpec()
        tools = spec.to_tool_list()
        desc_map = {t.metadata.name: t.metadata.description for t in tools}
        assert "Firecracker" in desc_map["omnirun_execute"]
        assert "shell" in desc_map["omnirun_shell"].lower()
        assert "Write" in desc_map["omnirun_write_file"]
        assert "Read" in desc_map["omnirun_read_file"]

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_execute_code_returns_stdout(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb
        mock_result = MagicMock()
        mock_result.stdout = "hello"
        mock_result.stderr = ""
        mock_result.exit_code = 0
        mock_sb.commands.run.return_value = mock_result

        spec = OmniRunToolSpec()
        output = spec.execute_code("print('hello')")
        assert "hello" in output

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_execute_code_includes_stderr(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "traceback"
        mock_result.exit_code = 1
        mock_sb.commands.run.return_value = mock_result

        spec = OmniRunToolSpec()
        output = spec.execute_code("bad code")
        assert "STDERR: traceback" in output
        assert "Exit code: 1" in output

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_execute_code_no_output(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_result.exit_code = 0
        mock_sb.commands.run.return_value = mock_result

        spec = OmniRunToolSpec()
        output = spec.execute_code("pass")
        assert output == "(no output)"

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_run_shell(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb
        mock_result = MagicMock()
        mock_result.stdout = "Linux"
        mock_result.stderr = ""
        mock_result.exit_code = 0
        mock_sb.commands.run.return_value = mock_result

        spec = OmniRunToolSpec()
        output = spec.run_shell("uname")
        assert "Linux" in output

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_write_file(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb

        spec = OmniRunToolSpec()
        result = spec.write_file("/tmp/test.py", "x = 1")
        assert "Written 5 bytes" in result
        mock_sb.files.write.assert_called_once_with("/tmp/test.py", "x = 1")

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_read_file(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb
        mock_sb.files.read.return_value = "file contents"

        spec = OmniRunToolSpec()
        result = spec.read_file("/tmp/test.py")
        assert result == "file contents"

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_cleanup(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb

        spec = OmniRunToolSpec()
        spec._get_sandbox()
        spec.cleanup()
        mock_sb.kill.assert_called_once()
        assert spec._sandbox is None

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_sandbox_lazy_init(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        spec = OmniRunToolSpec()
        assert spec._sandbox is None
        mock_sandbox_cls.create.assert_not_called()

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb

        spec._get_sandbox()
        mock_sandbox_cls.create.assert_called_once_with("python-3.11", timeout=300)

    @patch("llama_index_tools_omnirun.tools.Sandbox")
    def test_sandbox_reused(self, mock_sandbox_cls):
        from llama_index_tools_omnirun import OmniRunToolSpec

        mock_sb = MagicMock()
        mock_sandbox_cls.create.return_value = mock_sb

        spec = OmniRunToolSpec()
        sb1 = spec._get_sandbox()
        sb2 = spec._get_sandbox()
        assert sb1 is sb2
        mock_sandbox_cls.create.assert_called_once()
