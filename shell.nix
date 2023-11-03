{ pkgs ? import <nixpkgs> {} , ...}:

with pkgs;
mkShell {
  buildInputs = [
    python39
    python39Packages.numpy
  ];
}