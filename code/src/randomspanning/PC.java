/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package randomspanning;


import Jama.Matrix;
import java.util.ArrayList;
import java.util.HashMap;


/**
 *
 * @author sirajs
 */
public class PC extends Matrix {
    private static final long serialVersionUID = 4387864900226806206L;
    protected String _ref = "";
    protected String _refid = "";
    public void setRef(String ref){_ref=ref;}
    public void setRef(String ref, String refid){
        _ref=ref; _refid=refid;
    }
    public String getRef(){return _ref;}
    public String getRefId(){return _refid;}
    
    public PC(int n) {
        super( new double[n][n] );
    }

    public PC(double[][] A) {
        super(A);
    }

    public boolean invert(int i, int j) {
        int N = getColumnDimension();
        if (i>=0&&j>=0&&i<N&&j<N) {
            double Aij = get(i, j);
            set(i, j, 1 / Aij);
            set(j, i, Aij);
            return true;
        }
        return false;
    }

    public void build() {
        int N = getColumnDimension();
        for(int i=0; i<N; i++){
        for(int j=0; j<N; j++){
            double Aij = get(i,j);
            double Aji = get(j,i);
            if(Aij<=0 && Aji>0){
                set(i,j, 1.0/Aji );
            }
        }}
    }

    public boolean swap(int i, int j) {
        int N = getColumnDimension();
        if (i>=0&&j>=0&&i<N&&j<N) {
            double Aij = get(i, j);
            double Aji = get(j, i);
            set(i, j, Aji);
            set(j, i, Aij);
            return true;
        }
        return false;
    }

    public boolean reverse(int i, int j) {
        int N = getColumnDimension();
        if (i>=0&&j>=0&&i<N&&j<N) {
            double Aij = get(i, j);
            Aij = (Aij<1)?1.01:0.99;
            set(i, j, Aij);
            set(j, i, 1/Aij);
            return true;
        }
        return false;
    }

    public double[] getScale() {
        return _scale;
    }
    public void setScale(double[] domain) {
        _scale = domain;
    }

    public static PC fromW(double[] w) {
        int N = w.length;
        PC mat = new PC(identity(N, N).getArray());
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                mat.set(i, j, w[i]/w[j]);
            }
        }
        return mat;
    }

    public void setn(int i, int j, double a) {
        set(i-1, j-1, a);
    }

    ArrayList<int[]> _vL = new ArrayList<int[]>();

    public static final double _maxRatioScale = 100;
    public static final double _thresholdEquivalence = 0.01;
    public double[] _scale = null;
    
    public String hashSpanningTree(PC tau){
        HashMap<Integer, Judgment> J = Matrix2Map();
        int[] v = new int[J.size()];
        String key = "_";
        for(int i=0; i<J.size(); i++){
            Judgment j = J.get(i);
            if( tau.get(j.i,j.j)>0 ){
                v[i] = 1;
            }else{
                v[i] = 0;
            }
            key += ""+v[i];
        }
        return key;
    }
    
    public HashMap<Integer, Judgment> Matrix2Map(){
        HashMap<Integer, Judgment> J = new HashMap<>();
        int m=0;
        for( int i=0; i<this.n(); i++ ){
            for( int j=i+1; j<this.n(); j++ ){
                if(this.get(i,j)>0){
                    J.put(m, new Judgment(m, i, j, this.get(i,j)) );
                    m++;
                }
            }
        }
        return J;
    }

    final ArrayList<Object[]> _prop = new ArrayList<Object[]>();
    
	public int rowProperties() {
		if(_prop.size()<=0){ calculateProperties(); }
		return _prop.size();
	}
	
	public int colProperties() {
		if(_prop.size()<=0){ calculateProperties(); }
		return 2;
	}
	
	public Object property(int row, int column) {
		if(_prop.size()<=0){ calculateProperties(); }
		Object[] obj = _prop.get(row);
		return obj[column];
	}

    private void calculateProperties() {
        Object[] obj; 
        
        obj= new Object[2];
        obj[0]="n"; obj[1]=n();
        _prop.add(obj);

        obj= new Object[2];
        obj[0]="L"; obj[1]=TournamentAnalyzer.findLoopsKendall(this).size();
        _prop.add(obj);
        
        obj= new Object[2];
        obj[0]="CR"; obj[1]=ConsistencyAnalyzer.CR(this);
        _prop.add(obj);

        obj= new Object[2];
        obj[0]="CM"; obj[1]=ConsistencyAnalyzer.CM(this);
        _prop.add(obj);

        obj= new Object[2];
        _theta 	= IndirectAnalyzer.congruence(this);
        obj[0]="Congruence"; obj[1]=IndirectAnalyzer.measure(_theta);
        _prop.add(obj);
        
        obj= new Object[2];
        _phi 	= IndirectAnalyzer.dissonance(this);
        obj[0]="Dissonance"; obj[1]=IndirectAnalyzer.measure(_phi);
        _prop.add(obj);
		
	}
    
	public int n(){
        return getRowDimension();
    }
	

    private PC _theta;
    private PC _phi;

}
