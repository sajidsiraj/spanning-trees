/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package randomspanning;

import Jama.Matrix;
import java.util.Arrays;
import java.util.ArrayList;


/**
 *
 * @author sirajs
 */
public class TournamentAnalyzer {

    static public int[] getScores(PC J) {
        int n = J.getRowDimension();
        int[] scores = new int[n];
        for (int i=0; i<n; i++) {
            for (int j=0; j<n; j++) {
                if(J.get(i, j)>1){
                    scores[i] += 1;
                }
            }
        }
        return scores;
    }

    static public ArrayList<int[]> listUpsets(PC J) {
        int n = J.getRowDimension();
        int[] scores = getScores(J);
        ArrayList<int[]> vRet = new ArrayList<>();
        for (int i=0; i<n; i++) {
            for (int j=0; j<n; j++) {
                int s = scores[j]-scores[i];
                if( J.get(i, j)>1 && s >= 0 ){
                    int[] upset = {i,j,s};
                    vRet.add(upset);
                }
            }
        }
        return vRet;
    }

    static public ArrayList<int[]> listMaxUpsets(PC J) {
        ArrayList<int[]> vUpsets = listUpsets(J);
        return listMaxUpsets(J, vUpsets);
    }

    static public ArrayList<int[]> listMaxUpsets(PC J, ArrayList<int[]> vUpsets) {
        if(vUpsets==null)vUpsets = listUpsets(J);
        ArrayList<int[]> vRet = new ArrayList<>();
        int nMax = -1;
        for (int[] upset : vUpsets) {
            if(upset[2]>nMax){
                nMax=upset[2];
                vRet = new ArrayList<>();
                vRet.add(upset);
            }else if(upset[2]==nMax){
                vRet.add(upset);
            }
        }
        return vRet;
    }

    static public PC findBetaMinsAlpha(PC J) {
        int n = J.getRowDimension();
        PC matOut = new PC(Matrix.identity(n,n).getArray());
        int[] scores = new int[n];

        for (int i = 0; i<n; i++) {
            for (int j = 0; j<n; j++) {
                if (J.get(i, j) > 1) {
                    scores[i] += 1;
                }
            }
        }

        for (int i = 0; i<n; i++) {
            for (int j = 0; j<n; j++) {
                if (J.get(i, j) > 1) {
                    matOut.set(i, j, scores[j] - scores[i]);
                } else {
                    matOut.set(i, j, -n*n);
                }
            }
        }
        return matOut;
    }

    static public double countLoopsGass(PC A) {
        int n = A.getRowDimension();

        int nMatches = 0;
        int[] s = new int[n];
        double fSumOfSq = 0.0;
        for (int i = 0; i < n; i++) {
            s[i] = 0;
            for (int j = 0; j < n; j++) {
                s[i] += A.get(i, j) > 1 ? 1.0 : 0.0;
            }
            nMatches += s[i];
            fSumOfSq += (s[i] * (s[i] - 1));
        }

        int nTotalMatches = n * (n - 1) / 2;
        if (nMatches != nTotalMatches) {
        }

        double loops = (n * (n - 1) * (n - 2) / 6) - (fSumOfSq / 2);
        return loops;
    }

    static public ArrayList<int[]> findLoopsJensen(PC J) {
        int n = J.getRowDimension();
        ArrayList<int[]> vLoops = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i != j) {
                    for (int k = 0; k < n; k++) {
                        if ((j != k) && (k != i)) {
                            int[] vLoop = {i, j, k};
                            Arrays.sort(vLoop);
                            boolean bFlag = true;
                            for (int[] vMem : vLoops) {
                                if (Arrays.equals(vMem, vLoop)) {
                                    bFlag = false;
                                }
                            }

                            double Rij = Math.log(J.get(i, j));
                            double Rik = Math.log(J.get(i, k));
                            double Rjk = Math.log(J.get(j, k));

                            if (Rij * Rik <= 0 && Rik * Rjk < 0) {
                                if (bFlag) {
                                    vLoops.add(vLoop);
                                }
                            }

                            if (Rij == 0 && Rik == 0 && Rjk != 0) {
                                if (bFlag) {
                                    vLoops.add(vLoop);
                                }
                            }
                        }
                    }
                }
            }
        }
        return vLoops;
    }

    static public ArrayList<int[]> findLoopsKendall(PC J) {
        int N = J.getRowDimension();
        ArrayList<int[]> vLoops = new ArrayList<>();

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (i != j) {
                    double a_ij = J.get(i, j);
                    for (int k = 0; k < N; k++) {
                        if ((j != k) && (k != i)) {
                            double a_ik = J.get(i, k);
                            double a_kj = J.get(k, j);
                            // test for missing judgement
                            if (a_ik>0 && a_kj>0 && a_ij>0)
                            if (a_ik > 1 && a_kj > 1 && a_ij < 1) {
                                int[] vLoop = {i, j, k};
                                Arrays.sort(vLoop);
                                boolean bFlag = true;
                                for (int[] vMem : vLoops) {
                                    if (Arrays.equals(vMem, vLoop)) {
                                        bFlag = false;
                                    }
                                }
                                if (bFlag) {
                                    vLoops.add(vLoop);
                                }
                            }
                        }
                    }
                }
            }
        }

        return vLoops;
    }

    static public ArrayList<int[]> getBlamedEdges(PC A){
        final int n = A.getRowDimension();
        PC blame = new PC(A.getArrayCopy());
        for( int i=0; i<n; i++){
            for( int j=0; j<n; j++ ){
                blame.set(i,j,0);
            }
        }

        ArrayList<int[]> vLoops = TournamentAnalyzer.findLoopsKendall(A);
        vLoops.stream().forEach((v) -> {
            for( int p=0; p<v.length; p++){
                for( int q=(p+1); q<v.length; q++ ){
                    int i=v[p]; int j=v[q];
                    if(A.get(i,j)>1){
                        blame.set(i, j, 1+blame.get(i, j) );
                    }else if(A.get(j,i)>1){
                        blame.set(j, i, 1+blame.get(j, i) );
                    }
                }
            }
        });
        ArrayList<int[]> vInLoops = new ArrayList<>();
        for( int i=0; i<n; i++){
            for( int j=0; j<n; j++ ){
                double x= blame.get(i,j);
                if( x>0 ){
                    int[] v = {i,j, (int)x};
                    vInLoops.add(v);
                }
            }
        }
        return vInLoops;
    }


}
