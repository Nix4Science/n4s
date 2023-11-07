{ python3Packages, fetchFromGitHub }:

python3Packages.buildPythonApplication rec {
    pname = "mop";
    version = "0.0.0";
    src = fetchFromGitHub {
        owner = "Nix4Science";
        repo = "mop";
        rev = "v${version}";
        sha256 = "sha256-vWeucqMeKL6OJWsTqfhIM53GQ/UqeiopBgrm70iuE8U=";
    };
    propagatedBuildInputs = with python3Packages; [
        pyyaml requests
    ];
}
