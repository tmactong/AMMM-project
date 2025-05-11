/*********************************************
 * OPL 22.1.1.0 Model
 * Author: tmactong
 * Creation Date: May 10, 2025 at 1:50:42 PM
 *********************************************/

 
int N=...;
range Members=1..N;
int m[Members][Members]=...;

dvar boolean Priority[Members][Members];
dvar int+ TopologicalOrder[Members];
dexpr int Income = sum(i in Members, j in Members) m[i][j] * Priority[i][j];

maximize Income;

subject to {
  forall(i in Members) {
    forall(j in Members: m[i][j] != 0 || m[j][i] != 0) {
      	// If member i has priority over member j, then member j has no priority over i
      	Priority[i][j] + Priority[j][i] == 1;
      	// each member appears before all the members it points to
      	TopologicalOrder[i] + 1 <= TopologicalOrder[j] + (1 - Priority[i][j]) * N;
    }
  }
}

execute DisplayResult {
  for (var i=1;i<=N;i++) {
    for (var j=1;j<=N;j++) {
      if (Priority[i][j] == 1) {
          writeln(i, ' -> ', j);
      } 
    }
  }
}
