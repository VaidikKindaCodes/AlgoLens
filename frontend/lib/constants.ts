import type { LanguageOption } from "@/types/workspace";

export const APP_NAME = "AlgoLens";

export const LANGUAGES: LanguageOption[] = [
  { id: "cpp", label: "C++ 20", monacoId: "cpp", extension: "cpp" },
  { id: "python", label: "Python 3", monacoId: "python", extension: "py" },
  { id: "java", label: "Java 21", monacoId: "java", extension: "java" },
  {
    id: "javascript",
    label: "JavaScript",
    monacoId: "javascript",
    extension: "js",
  },
  { id: "go", label: "Go 1.23", monacoId: "go", extension: "go" },
];

export const DEFAULT_CODE: Record<LanguageOption["id"], string> = {
  cpp: `#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Write your solution here
    return 0;
}`,
  python: `import sys

def solve() -> None:
    # Write your solution here
    pass

if __name__ == "__main__":
    solve()
`,
  java: `import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        // Write your solution here
    }

    static class FastScanner {
        private final InputStream in;
        FastScanner(InputStream in) { this.in = in; }
    }
}
`,
  javascript: `const fs = require("fs");
const input = fs.readFileSync(0, "utf8").trim();

function solve(input) {
  // Write your solution here
}

solve(input);
`,
  go: `package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    in := bufio.NewReader(os.Stdin)
    out := bufio.NewWriter(os.Stdout)
    defer out.Flush()

    _ = in
    fmt.Fprintln(out)
}
`,
};
