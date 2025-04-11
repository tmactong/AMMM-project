/*********************************************
 * OPL 22.1.1.0 Model
 * Author: tmactong
 * Creation Date: Apr 3, 2025 at 10:12:47 AM
 *********************************************/

 
int N=...;
range Members=1..N;
int m[Members][Members]=...;
{int} MemberSet = asSet(Members);

int TotalChainCount;

execute CalculateDeduplicateLoopCount {
  
  function CalculateCombinationCount(allMemberCount, chosenMemberCount) {
    var CombinationCount = 1;
    for (var i=allMemberCount;i>allMemberCount-chosenMemberCount;i--) {
      CombinationCount *= i;
    }
    for (var j=1;j<=chosenMemberCount;j++) {
      CombinationCount /= j;
    }
    return CombinationCount;
  }

  function CalculatePermutationCount(memberCount) {
    var permutationCount = 1;
    for (var i=memberCount;i>=1;i--) {
      permutationCount *= i; 
    }
    return permutationCount;
  }
  
  function CalculateSequenceCount(memberCount) {
    var totalSequenceCount = 0;
    for (var i=0;i<memberCount-2;i++) {
      var sequenceCount = 1;
      // moving member count = i
      // availablely moving count = memberCount -3
      // residual member count = memberCount - 2 - i;
      for (var j=1;j<=i;j++) {
        sequenceCount *= memberCount - 2 -j;
      }
      var permutationCount = CalculatePermutationCount(memberCount-2-i);
      sequenceCount *= permutationCount;
      totalSequenceCount += sequenceCount; 
    }
    return totalSequenceCount;
  }
  
  for (var i=3;i<=N;i++) {
    var combinationCount = CalculateCombinationCount(N, i);
    var sequenceCount = CalculateSequenceCount(i);
    TotalChainCount += combinationCount * sequenceCount;
  }
  writeln('total chain count: ', TotalChainCount);
}

int MemberChains[1..TotalChainCount][1..N+1];

execute GetNoRepetitionSequences {
  
  function discardBuiltinKeys(sparseArray) {
    var idx = 0;
    var newSparseArray = new Array();
    for (var i in sparseArray) {
      if ( i != 'toString' ) {
        if ( i != 'join') {
          if ( i != 'reverse') {
            if ( i != 'sort') {
              newSparseArray[idx] = sparseArray[i].split(",");
      	      idx += 1;
      	    }
      	  }
      	}
      }
    }
    return newSparseArray;
  }
  
  function getCombinations(selectedMembers,selectedMemberCount,neededMember, combinations) {
    var lastestSelectedMember = 0;
    if (selectedMemberCount > 0) {
      lastestSelectedMember = selectedMembers[selectedMemberCount-1];
    }
    if (selectedMemberCount + 1 == neededMember) {
      // last round
      for (var j=lastestSelectedMember+1;j<=Opl.card(MemberSet);j++) {
        var newSelectedMembers = new Array();
        for (var k=0;k<=selectedMemberCount-1;k++) {
          newSelectedMembers[k] = selectedMembers[k];
        }
        newSelectedMembers[selectedMemberCount] = j;
        combinations[newSelectedMembers.join()] = newSelectedMembers.join();
      }
    } else {
      for (var j=lastestSelectedMember+1;j<=Opl.card(MemberSet);j++) {
        var newSelectedMembers = new Array();
        var newSelectedMemberCount = selectedMemberCount + 1;
        if ( lastestSelectedMember != 0) {
          for (var k=0;k<=selectedMemberCount-1;k++) {
          	newSelectedMembers[k] = selectedMembers[k];
          }
        }
        newSelectedMembers[selectedMemberCount] = j; 
        getCombinations(newSelectedMembers, newSelectedMemberCount, neededMember, combinations);
      }
    }
  }
  
  function getPermutations(selectedMembers,selectedMemberCount, residualMembers, neededMember, permutations) {
    if (selectedMemberCount + 1 == neededMember) {
      // last round
      var newSelectedMembers = new Array();
      for (var k=0;k<=selectedMemberCount-1;k++) {
        newSelectedMembers[k] = selectedMembers[k];
      }
      newSelectedMembers[selectedMemberCount] = residualMembers[0];
      permutations[newSelectedMembers.join()] = newSelectedMembers.join();
    } else {
      for (var j=0;j<=residualMembers.length-1;j++) {
        var newSelectedMembers = new Array();
        var newResidualMembers = new Array();
        var newSelectedMemberCount = selectedMemberCount + 1;
        if ( selectedMemberCount != 0) {
          for (var k=0;k<=selectedMemberCount-1;k++) {
          	newSelectedMembers[k] = selectedMembers[k];
          }
        }
        newSelectedMembers[selectedMemberCount] = residualMembers[j];
        for (var l=0,m=0;l<=residualMembers.length-1;l++) {
          if (l != j) {
            newResidualMembers[m] = residualMembers[l];
            m += 1;
          }  
        }
        getPermutations(newSelectedMembers, newSelectedMemberCount, newResidualMembers, neededMember, permutations);
      }
    }
  }
  
  function generateSequences(allMembers) {
    var sequences = new Array();
    var count = 0;
    var repetitions = allMembers.length - 2;
    for (var i=0;i<repetitions;i++) {
      // prefix 1,allMembers[i+1]
      var residualMembers = new Array();
      var movingMembers = new Array();
      
      // get movingMembers
      for (var j=1,k=0;j<=i,k<i;j++,k++) {
        movingMembers[k] = allMembers[j];
      }
      for (var j=i+2;j<=allMembers.length-2,k<i;j++,k++) {
        movingMembers[k] = allMembers[j];  
      }
      
      // get residualMembers
      var k =0;
      for (var j=1;j<=i;j++) {
        residualMembers[k] = allMembers[j];
        k += 1;
      }
      for (var j=i+2;j<=allMembers.length-1;j++) {
        residualMembers[k] = allMembers[j];
        k += 1;
      }
      //writeln('movingMembers=', movingMembers.join(""), '; residualMembers=', residualMembers.join(""));
      
      if ( residualMembers.length > 1) { 
        var permutations = new Array();
      	var selectedMembers = new Array();
      	getPermutations(selectedMembers, 0, residualMembers, residualMembers.length, permutations);
      	// discard 'toString', 'join', 'reverse', 'sort' element from permutations
      	var permutations = discardBuiltinKeys(permutations);
      	for (var p=0;p<=permutations.length-1;p++) {
      	  var endsWithMovingMember = 0;
      	  for (var l=0;l<=movingMembers.length-1;l++) {
      	    if (permutations[p][residualMembers.length - 1] == movingMembers[l]) {
      	      endsWithMovingMember = 1;
      	    }
          }
          if ( endsWithMovingMember == 0) {
            sequences[count] = new Array(1, allMembers[i+1]);
            for (var j=0;j<permutations[p].length;j++) {
              sequences[count][j+2] = permutations[p][j];
            }
            count += 1;
          }
        }
      } else {
        sequences[0] = new Array(1, allMembers[i+1]);
        sequences[count][2] = residualMembers[0];
      }
    }
    return sequences;
  }
  
  var idx = 1;
  for (var neededMemberCount=3;neededMemberCount<=N;neededMemberCount++) {
    writeln('member count: ', neededMemberCount);
    // construct members
    var members = new Array();
    for (var i=0;i<=neededMemberCount-1;i++) {
      members[i] = i+1;
    }
    var sequences = generateSequences(members)
    
    var selectedMembers = new Array();
    var combinations = new Array();
  	getCombinations(selectedMembers, 0, neededMemberCount, combinations);
  	combinations = discardBuiltinKeys(combinations);
  	for (var i=0;i<=combinations.length-1;i++) {
  	  // writeln('combination: ', combinations[i].join(""));
  	  for (var j=0;j<=sequences.length-1;j++) {
    	// writeln('sequence: ', sequences[j].join(""));
    	var chain = new Array();
    	for (var k=1;k<=neededMemberCount;k++) {
    	  //writeln('idx=', idx, '; k=', k, ' sequence=', sequences[j].join(), '; combination=', combinations[i].join());
    	  MemberChains[idx][k] = combinations[i][sequences[j][k-1]-1];
    	}
    	MemberChains[idx][neededMemberCount+1] = combinations[i][sequences[j][0]-1];
    	idx += 1;	
      }	
  	}
  }
  writeln('member cycles generated');
  
  //for (var i=1;i<=TotalChainCount;i++) {
  //  writeln(MemberChains[i]);
  //}
}



dvar boolean Priority[Members][Members];
dexpr int Income = sum(i in Members, j in Members) m[i][j] * Priority[i][j];

maximize Income;

subject to {
  // If member i has priority over member j, then member j has no priority over i
  forall(i in Members) {
    forall(j in Members: i != j) {
      Priority[i][j] + Priority[j][i] == 1;
    }
  }
  // for every member chain, the sum of priorities is between 1 and 2, i.e., no loops of priorities are formed.
  forall(i in 1..TotalChainCount) {
    sum(j in 2..N+1:MemberChains[i][j]!=0) Priority[MemberChains[i][j]][MemberChains[i][j-1]] >= 1;
    sum(j in 2..N+1:MemberChains[i][j]!=0) Priority[MemberChains[i][j-1]][MemberChains[i][j]] >= 1;
  }
}

execute DisplayResult {
  for (var i=1;i<=N;i++) {
    for (var j=1;j<=N;j++) {
      if (Priority[i][j] == 1) {
        if (m[i][j] != 0) {
          writeln(i, ' -> ', j);
        }  
      } 
    }
  }
}

