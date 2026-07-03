/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package randomspanning;


/**
 *
 * @author busssir
 */
public class Example_SaatySchool extends ExampleBase {
    
    public Example_SaatySchool(){
        _name = "SaatySchool";
    }
    
    @Override
    public PC getPCM(int id){
        switch(id){
            case 0: return get_top();
            case 1: return get_c1();
            case 2: return get_c2();
            case 3: return get_c3();
            case 4: return get_c4();
            case 5: return get_c5();
            case 6: return get_c6();
        }
        return null;
    }    
    
    @Override
    public PC get_top(){
        PC c1 = createPC(6);
        c1.set(0, 1, 4);
        c1.set(0, 2, 3);
        c1.set(0, 3, 1);
        c1.set(0, 4, 3);
        c1.set(0, 5, 4);
        
        c1.set(1, 2, 7);
        c1.set(1, 3, 3);
        c1.set(1, 4, 1.0/5);
        c1.set(1, 5, 1);
        
        c1.set(2, 3, 1.0/5);
        c1.set(2, 4, 1.0/5);
        c1.set(2, 5, 1.0/6);
        
        c1.set(3, 4, 1);
        c1.set(3, 5, 1.0/3);
        
        c1.set(4, 5, 3);
        
        c1.build();
        
        return c1;
    }
    
    public PC get_c1(){
        PC c1 = createPC(3);
        c1.set(0, 1, 1.0/3);
        c1.set(0, 2, 1.0/2);
        c1.set(1, 2, 3);
        c1.build();
        return c1;
    }
    
    public PC get_c2(){
        PC c1 = createPC(3);
        c1.set(0, 1, 1);
        c1.set(0, 2, 1);
        c1.set(1, 2, 1);
        c1.build();
        return c1;
    }

    public PC get_c3(){
        PC c1 = createPC(3);
        c1.set(0, 1, 5);
        c1.set(0, 2, 1);
        c1.set(1, 2, 1.0/5);
        c1.build();
        return c1;
    }

    public PC get_c4(){
        PC c1 = createPC(3);
        c1.set(0, 1, 9);
        c1.set(0, 2, 7);
        c1.set(1, 2, 1.0/5);
        c1.build();
        return c1;
    }

    public PC get_c5(){
        PC c1 = createPC(3);
        c1.set(0, 1, 1.0/2);
        c1.set(0, 2, 1);
        c1.set(1, 2, 2);
        c1.build();
        return c1;
    }
    
    public static PC get_c6(){
        PC c1 = createPC(3);
        c1.set(0, 1, 6);
        c1.set(0, 2, 4);
        c1.set(1, 2, 1/3.0);
        c1.build();
        return c1;
    }    


}
