{ buildGoModule, fetchFromGitHub }:

let
  version = "v0.3";
  repo = fetchFromGitHub {
    owner = "GuilloteauQ";
    repo = "nix-shell-container";
    rev = version;
    sha256 = "sha256-w9vSETzStHMkXCa4U2e5P55C53gg7mzw1dB6UiQpTf0=";
  };
in buildGoModule {
  name = "gotainer";
  inherit version;
  src = "${repo}/gotainer";
  vendorSha256 = null;
}
