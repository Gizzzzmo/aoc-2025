{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake {  inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];
    perSystem = { config, self', inputs', pkgs, system, ... }: {
      # Per-system attributes can be defined here. The self' and inputs'
      # module parameters provide easy access to attributes of the same
      # system.
      devShells = {
        default = pkgs.mkShell {
          packages = with pkgs; [
            python313
            python313Packages.numpy
            python313Packages.scikit-learn
            basedpyright
          ];
        };
      };
    };
  };
}
